# Architecture

This document walks through the full data pipeline — from raw API ingestion to analytics-ready tables — covering each component, how they connect, and the design decisions behind it.

## Architecture Diagram

<iframe width="768" height="496" src="https://miro.com/app/live-embed/uXjVG24Xf7s=/?focusWidget=3458764662592067466&embedMode=view_only_without_ui&embedId=571479114836" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>

For a clearer view, open the [interactive Miro board](https://miro.com/app/live-embed/uXjVG24Xf7s=/?focusWidget=3458764662592067466&embedMode=view_only_without_ui&embedId=571479114836).

![Architecture Diagram](images/architecture-diagram.jpeg)

---

## Orchestration — Airflow

[Apache Airflow](https://airflow.apache.org/) runs on an [EC2](https://docs.aws.amazon.com/ec2/latest/userguide/concepts.html) instance and is the central orchestrator for the entire pipeline.

The DAG `brewery_pipeline` is scheduled to run daily at **7:00 AM UTC**, firing each step in sequence and passing outputs between tasks through [XCom](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html).

**Version:** Apache Airflow 2.10.3
**Providers:** [apache-airflow-providers-amazon](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/index.html) 8.26.0

The pipeline has four tasks:

```
invoke_openbrewery_lambda → parse_lambda_response → bronze_to_silver → silver_to_gold
```

The first task fires the Lambda function. The second parses the Lambda response and pulls out two values — `filename` and `ingestion_date` — which get injected as job arguments into the two downstream Glue steps.

![Airflow DAG](images/airflow-pipeline-dag.png)

DAG file: [dags/brewery_pipeline.py](../dags/brewery_pipeline.py)

---

## Ingestion — AWS Lambda

The [Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) function `BronzeApiCaptureBreweries` pulls a full snapshot from the [Open Brewery DB API](https://openbrewerydb.org/documentation). Before paginating, it calls the `/meta` endpoint to get the total record count and calculate exactly how many pages are needed (up to 200 records per request). All records are collected, serialized as JSON, and uploaded to S3 in a single file.

**Target bucket:** `bws-dl-bronze-sae-prd`

**S3 path pattern:**
```
breweries/tb_breweries/ingestion_date=YYYY-MM-DD/data_HHMMSS.json
```

After the upload completes, the function returns `filename` and `ingestion_date` to Airflow. Those values travel through XCom into the parameters of the next Glue jobs.

**Retry logic:** On HTTP errors or timeouts, each request retries up to 3 times with exponential backoff before raising an exception.

**Notifications** are configured via the `notification_params` table in [DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html). This table controls which email addresses receive alerts on failure, warning, or success. See [aws/dynamo_params.md](../aws/dynamo_params.md) for the full parameter reference.

Uses the shared `utils` and `logs` modules. See [aws/modules.md](../aws/modules.md) for details.

Script: [aws/lambda_scripts/BronzeApiCaptureBreweries.py](../aws/lambda_scripts/BronzeApiCaptureBreweries.py)

---

## Bronze Layer — Raw Data

The Bronze S3 bucket stores raw JSON files exactly as returned by the API — no transformations applied. This layer is the safety net of the pipeline: if anything goes wrong downstream, data can always be reprocessed from here without hitting the API again.

---

## Bronze to Silver — AWS Glue (PySpark)

The [Glue](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html) job `bronze_to_silver` reads the JSON file from the Bronze layer and converts it into [Parquet](https://parquet.apache.org/) format. Parquet is a columnar storage format that reduces query costs and execution time on Athena significantly compared to JSON — particularly when filtering on specific columns.

Data is written to the Silver bucket partitioned by **country** and **state**, so location-based queries only scan the relevant partitions instead of the full dataset.

**What this job does:**
- Reads the exact file passed by Airflow (`--file_name` and `--dt_ref`)
- Applies schema casting, null handling, and column standardization
- Runs data quality checks configured in DynamoDB (`quality_params`) using the [Quality module](../aws/modules/quality.py)
- Writes the clean result as Parquet, partitioned by country and state

**Designed as a generic processing engine:**
This job reads all its configuration from DynamoDB (`ingestion_params`) — source paths, schema definitions, quality rules. Pass it different parameters and it processes a completely different dataset without any code changes. This makes it reusable across multiple ingestion pipelines.

An Athena table is already set up pointing at the Silver bucket. A query screenshot will be added once available.

Uses the `utils`, `logs`, and `quality` modules. See [aws/modules.md](../aws/modules.md) for details. For DynamoDB parameters, see [aws/dynamo_params.md](../aws/dynamo_params.md).

Script: [aws/glue_scripts/bronze_to_silver.py](../aws/glue_scripts/bronze_to_silver.py)

---

## Silver to Gold — AWS Glue (PySpark)

The [Glue](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html) job `silver_to_gold` reads clean Silver data and produces a pre-aggregated table in the Gold layer. Instead of hardcoding the transformation logic inside the job, the SQL query is stored as a `.sql` file in S3 and loaded at runtime. This keeps business logic versioned and separated from execution code.

The job runs that SQL against the Glue/Iceberg catalog inside a Spark environment and writes results to an [Apache Iceberg](https://iceberg.apache.org/) table.

**Why Iceberg?**
Iceberg is an open table format designed for large-scale data lakes. It adds ACID transactions, schema evolution, and time-travel queries on top of S3-backed storage — making the Gold layer reliable and queryable with standard SQL tools like Athena. More on [Iceberg's benefits here](https://iceberg.apache.org/docs/latest/).

**What the SQL does:**
Groups breweries by country, state, and brewery type, counting how many exist per combination. This powers the main analytics view in the Streamlit dashboard.

SQL file: [aws/sql/gold/tb_ft_breweries_agg.sql](../aws/sql/gold/tb_ft_breweries_agg.sql)

**Also a generic engine:**
Like the Bronze to Silver job, configuration is pulled from DynamoDB (`refined_params`). Point it at a different SQL file and target table and it processes an entirely different aggregation without touching the code.

An Athena table is already set up pointing at the Gold bucket. A query screenshot will be added once available.

Uses the `utils`, `logs`, and `quality` modules. See [aws/modules.md](../aws/modules.md) for details. For DynamoDB parameters, see [aws/dynamo_params.md](../aws/dynamo_params.md).

Script: [aws/glue_scripts/silver_to_gold.py](../aws/glue_scripts/silver_to_gold.py)