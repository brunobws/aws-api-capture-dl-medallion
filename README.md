# Brewery Data Lake on AWS

![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Great Expectations](https://img.shields.io/badge/Great_Expectations-FF6B6B?style=for-the-badge&logoColor=white)

A production-grade data lake that ingests brewery data from the [Open Brewery DB API](https://openbrewerydb.org/), transforms it through a three-tier Medallion Architecture, and serves analytics via a Streamlit dashboard. Covers 8,000+ breweries across multiple countries, running on AWS with modularized logging, automated data quality testing, and email notifications for pipeline failures.

## Table of Contents

- [Live Dashboard](#live-dashboard)
- [Architecture Overview](#architecture-overview)
- [How It Works](#how-it-works)
- [Cloud Setup](#cloud-setup)
- [Technology Stack](#technology-stack)
- [Key Features](#key-features)
- [Documentation](#documentation)
- [Code Organization](#code-organization)
- [Infrastructure & Security](#infrastructure--security)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Questions or Feedback](#questions-or-feedback)

<a id="live-dashboard"></a>

## Live Dashboard 

**Access the dashboard:** http://56.124.50.116:8501/

![Dashboard Screenshot](docs/images/dashboard-screenshot.png)

Interactive analytics with three main sections:

- **Analytics** – Browse brewery data, apply filters, and view interactive graphs showing trends and distributions
- **Observability** – Real-time logs showing successful pipeline runs, errors, and performance metrics with visual charts
- **Data Quality** – Data validation results, completeness scores, and anomalies detected during processing

Watch demo videos to see the dashboard in action:

- [Analytics Dashboard Demo](docs/videos/01-analytics-dashboard-demo.mp4) (3 min)
- [Observability Logs Demo](docs/videos/02-observability-logs-demo.mp4) (2.2 min)
- [Data Quality Demo](docs/videos/03-data-quality-demo.mp4) (1.8 min)

For detailed dashboard documentation, see [Streamlit Guide](docs/dashboard.md).

<a id="architecture-overview"></a>

## Architecture Overview

![Brewery Data Lake Architecture](docs/images/architecture-diagram.jpeg)

The pipeline runs on a fully serverless AWS stack — except for the EC2 instance that hosts Airflow and the Streamlit dashboard. Data flows through three layers:

- **Bronze** – Raw JSON from the Open Brewery DB API, preserved as-is in S3 for full reprocessability
- **Silver** – PySpark-transformed [Parquet](https://parquet.apache.org/) files, partitioned by country and state for efficient querying
- **Gold** – Pre-aggregated [Apache Iceberg](https://iceberg.apache.org/) table with brewery counts by type and location, queryable via Athena

[Full architecture documentation →](docs/architecture.md) · [Interactive Miro board →](https://miro.com/app/live-embed/uXjVG24Xf7s=/?focusWidget=3458764662592067466&embedMode=view_only_without_ui&embedId=571479114836)

<a id="how-it-works"></a>

## How It Works

Daily at 7:00 AM UTC, the Airflow DAG triggers the following automated workflow:

**Data flow:**

1. **Ingestion** – AWS Lambda calls the Open Brewery DB API, handles pagination, and stores raw JSON in S3 Bronze
2. **Bronze Layer** – Raw data preserved as-is for disaster recovery and reprocessing
3. **Silver Layer** – AWS Glue applies PySpark transformations: clean column names, handle nulls, remove duplicates, partition by location, store as [Parquet](https://parquet.apache.org/) for efficient columnar storage
4. **Gold Layer** – AWS Glue creates pre-aggregated analytics: count of breweries by type and location, stored in [Apache Iceberg](https://iceberg.apache.org/) format for ACID transactions

**Platform capabilities running across every execution:**

5. **Execution Logging** – Each component (Lambda, Glue jobs) writes structured execution logs to a centralized Athena table `execution_logs`, partitioned by execution date, with step-level timing
6. **Data Quality** – Automated validation tests for completeness, accuracy, and consistency across all layers; quality results stored in a dedicated Athena `quality_logs` table with pass/fail status and email notifications
7. **Email Alerts** – Configurable email notifications on failures and warnings using [AWS SES](https://docs.aws.amazon.com/ses/), managed via DynamoDB `notification_params` table
8. **Monitoring** – [AWS CloudWatch](https://docs.aws.amazon.com/cloudwatch/) captures infrastructure-level metrics for Lambda and Glue; the primary observability layer is the custom `execution_logs` and `quality_logs` Athena tables, which provide full execution context for debugging and auditing

<a id="cloud-setup"></a>

## Cloud Setup ☁️

All components run on AWS infrastructure with zero local setup required.

A dedicated read-only user was created for you to safely explore the data lake. Access it with the credentials below – no need to install any software or configure anything locally.

```
AWS Console: https://580148408154.signin.aws.amazon.com/console
User: datalake-reader
```

Password: [Request access via WhatsApp](https://wa.me/5515997595138?text=Hi%2C+I%27d+like+to+request+the+read-only+AWS+console+password+for+the+Brewery+Data+Lake+project.)

With read-only access, you can:
- Browse S3 Bronze, Silver, Gold, and Logs layers
- Query Athena tables: Gold layer analytics, execution logs, data quality results
- Explore table schemas in AWS Glue Catalog
- View pipeline execution records and audit trails
- Access DynamoDB parameter tables to see configuration and notification settings
- View registered email addresses in Amazon SES

You cannot:
- Delete, edit, or create any resources
- Access any services outside of S3, Athena, Glue Catalog, DynamoDB, and SES
- Access any AWS regions outside the current one

<a id="technology-stack"></a>

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Cloud** | [AWS Lambda](https://docs.aws.amazon.com/lambda/), [Glue](https://docs.aws.amazon.com/glue/), [Athena](https://docs.aws.amazon.com/athena/), [S3](https://docs.aws.amazon.com/s3/), [DynamoDB](https://docs.aws.amazon.com/dynamodb/), [SES](https://docs.aws.amazon.com/ses/), [IAM](https://docs.aws.amazon.com/iam/), [EC2](https://docs.aws.amazon.com/ec2/), [CloudWatch](https://docs.aws.amazon.com/cloudwatch/) |
| **Orchestration** | Apache Airflow (Docker on EC2) |
| **Processing** | Python, PySpark |
| **Dashboard** | Streamlit (Docker on EC2) |
| **Data Format** | [Parquet](https://parquet.apache.org/) (Silver), [Apache Iceberg](https://iceberg.apache.org/) (Gold) |
| **Data Quality** | [Great Expectations](https://docs.greatexpectations.io/) |
| **Logging** | AWS CloudWatch, S3, Athena |

<a id="key-features"></a>

## Key Features

**Modularized Logging** – All components (Lambda, Glue jobs) use a [centralized Logs class](aws/modules/logs.py) that writes structured execution records with step-level timing to an Athena table. Each log includes job name, status, warnings, errors, and custom metadata.

**Data Quality Framework** – Automated validation tests built on [Great Expectations](https://docs.greatexpectations.io/) check data completeness, accuracy, and consistency at each layer. Quality metrics are stored in Athena for historical analysis and trend detection. See [quality module](aws/modules/quality.py).

**Email Alerting** – Configurable email notifications using [AWS SES](https://docs.aws.amazon.com/ses/) for pipeline failures and warnings. Alert recipients and thresholds are managed in DynamoDB.

**Generic Processing Engines** – Both Glue jobs are designed as configuration-driven engines. Pass different DynamoDB parameters and they process entirely different datasets without touching the code.

**Automated Retry Logic** – Failed Lambda and Glue jobs automatically retry with exponential backoff, reducing transient failures.

**Optimized Storage** – Silver and Gold layers use partitioning by location for query performance. Gold layer uses [Apache Iceberg](https://iceberg.apache.org/) for ACID transactions and schema evolution.

**DynamoDB Configuration** – Pipeline parameters, notification settings, and job configurations stored in DynamoDB tables for easy management without code changes.

**Unit Tests** – Core shared functions covered by 27 pytest tests, runnable fully offline with no AWS dependencies. See [tests/](tests/).

<a id="documentation"></a>

## Documentation

- [Architecture](docs/architecture.md) – Design patterns, data flow, component details
- [Dashboard Guide](docs/dashboard.md) – Using Streamlit analytics
- [Modules](docs/modules.md) – Shared Python modules: Logs, Quality, AwsManager
- [DynamoDB Parameters](docs/dynamo_params.md) – Pipeline configuration tables

<a id="code-organization"></a>

## Code Organization 📂

- [Lambda Scripts](aws/lambda_scripts/) – API ingestion and S3 cleanup
- [Glue ETL Jobs](aws/glue_scripts/) – Bronze→Silver→Gold transformations
- [Shared Modules](aws/modules/) – Centralized Logs class, AWS utilities, PySpark helpers, data quality functions
- [Airflow DAG](dags/brewery_pipeline.py) – Pipeline orchestration
- [Streamlit Dashboard](streamlit_app/) – Analytics interface
- [Unit Tests](tests/) – pytest suite for shared modules, runs fully offline

<a id="infrastructure--security"></a>

## Infrastructure & Security 

**Serverless Design** – [Lambda](https://docs.aws.amazon.com/lambda/), [Glue](https://docs.aws.amazon.com/glue/), and [Athena](https://docs.aws.amazon.com/athena/) scale automatically with zero infrastructure management. Pay only for what you use.

**EC2 Services** – Streamlit dashboard and Apache Airflow run in Docker containers on a single EC2 instance with a fixed Elastic IP, ensuring 24/7 availability with a stable address.

**Security Controls** – Read-only IAM user provided for safe exploration. All S3 data encrypted at rest using [AWS SSE](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryption.html). DynamoDB tables encrypted using [AWS KMS](https://docs.aws.amazon.com/kms/). Public API (no authentication secrets required). All credentials for internal services loaded from EC2 IAM roles.

**Audit Logging** – [CloudWatch](https://docs.aws.amazon.com/cloudwatch/) captures all API calls and data access for compliance and troubleshooting.

See the [Architecture — Security section](docs/architecture.md#security) for detailed IAM, VPC, and encryption configuration.

---

<a id="testing"></a>

## Testing

Unit tests cover the shared `support.py` module — pure Python functions with no AWS dependencies, runnable fully offline.

**Install pytest:**
```bash
pip install pytest
```

**Run all tests:**
```bash
pytest tests/ -v
# or
make test
```

**Expected output:**
```
tests/test_support.py::TestSummarizeException::test_returns_empty_string_for_none PASSED
tests/test_support.py::TestSummarizeException::test_returns_empty_string_for_empty_file_sentinel PASSED
tests/test_support.py::TestGetDateAndTime::test_format_is_correct PASSED
...
27 passed in 0.3s
```

See [tests/test_support.py](tests/test_support.py) for the full test suite.

---

<a id="roadmap"></a>

## Roadmap

Future enhancements planned for this project:

- **Custom domain with HTTPS** – Replace the raw IP:port access for the Streamlit dashboard and Airflow UI with a custom domain, SSL certificate via ACM, and an Nginx reverse proxy — making both services accessible through clean, secure URLs

- **Unit tests** – ✅ Implemented for `support.py` using pytest (27 tests, runs fully offline). Coverage planned for `logs.py` and `utils.py` with boto3 mocks. See [tests/](tests/).

- **Containerized deployment** – ✅ Airflow and Streamlit run in isolated Docker containers on a single EC2 instance, managed via Docker Compose. See [docker/](docker/).

- **Monitoring and alerting** – ✅ Full observability stack: structured execution logs written to Athena (`execution_logs`), automated data quality checks via Great Expectations (`quality_logs`), and color-coded HTML email notifications via AWS SES on failure, warning, and success with a dashboard to see the observability. See [Modules](docs/modules.md).

- **Configuration-driven pipeline** – ✅ Both Glue jobs are generic engines driven entirely by DynamoDB parameters — no code changes needed to onboard a new data source. Schema, partitioning, quality checks, and alert recipients are all externalized. See [DynamoDB Parameters](docs/dynamo_params.md).

- **CI/CD Pipeline** – GitHub Actions workflow that runs tests and linting on every push, then automatically packages and deploys Lambda functions and Glue scripts to the corresponding AWS environment

- **Infrastructure as Code** – Provision the entire AWS stack (S3 buckets, Lambda, Glue jobs, DynamoDB tables, IAM roles, EC2 security groups) using Terraform, enabling reproducible deployments from scratch with a single command

- **Multi-environment support** – Extend the existing `env` parameter pattern to a structured dev/prd pipeline with separate DynamoDB configurations, S3 prefixes, and Airflow connections per environment

---

<a id="questions-or-feedback"></a>

## Questions or Feedback

Thanks for reading! If you have any questions about the pipeline or would like to discuss the architecture, feel free to reach out.

**Contact:**
- Email: brun0ws@outlook.com
- LinkedIn: https://www.linkedin.com/in/brunowds/
- WhatsApp: https://wa.me/5515997595138
