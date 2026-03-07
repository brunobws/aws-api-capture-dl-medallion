# Brewery Data Lake on AWS

![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apache-spark&logoColor=white)

A production-grade data lake that ingests brewery data from the [Open Brewery DB API](https://openbrewerydb.org/), processes it through a Medallion Architecture (Bronze → Silver → Gold), and serves interactive analytics. The entire pipeline is cloud-native on AWS with real-time monitoring and automated orchestration.

## 🎬 Live Dashboard

**→ [Access the Analytics Dashboard](http://56.124.50.116:8501/)**

Explore real brewery data with interactive filters, visualizations, and exports. The dashboard features three main sections:

- **Analytics** – Browse brewery data with real-time filtering and custom queries
- **Observability** – Monitor pipeline health, execution times, and data quality metrics
- **Data Quality** – View validation results, anomalies, and completeness scores

## 🏗️ Architecture Overview

```
Open Brewery API
        ↓
AWS Lambda (Daily Ingestion)
        ↓
S3 Bronze Layer (Raw JSON)
        ↓
AWS Glue ETL (PySpark)
        ↓
S3 Silver Layer (Parquet, Partitioned by Location)
        ↓
AWS Glue ETL (PySpark)
        ↓
S3 Gold Layer (Apache Iceberg, Pre-aggregated Analytics)
        ↓
AWS Athena (SQL Query Engine)
        ↓
Streamlit Dashboard (EC2) + Apache Airflow (EC2)
```

**[→ View detailed architecture with diagrams and security model](docs/architecture.md)**

## ⚡ Quick Start

**No local setup required.** The entire pipeline runs serverlessly on AWS. Visit the dashboard link above to see it in action.

To explore the data lake directly:

```
AWS Console: https://580148408154.signin.aws.amazon.com/console
User: datalake-reader
Password: [Provided separately via secure channel]
```

With read-only access, you can:
- Browse S3 Bronze/Silver/Gold layers
- Write SQL queries in Amazon Athena
- Explore table schemas in AWS Glue Catalog
- Monitor pipeline runs in CloudWatch

## 🔄 How the Pipeline Works

**Daily Schedule:** 7:00 AM UTC

1. **Ingestion** – AWS Lambda invokes the Open Brewery DB API and dumps raw JSON to S3 Bronze
2. **Bronze Layer** – Unmodified API responses, stored for disaster recovery
3. **Silver Layer** – Data cleaning, deduplication, and partitioning by location (Parquet format)
4. **Gold Layer** – Pre-aggregated analytics: count of breweries by type and location (Apache Iceberg format)
5. **Monitoring** – CloudWatch tracks metrics, logs, and data quality; alerts on failures
6. **Visualization** – Streamlit dashboard queries Athena and displays results in real-time

The entire workflow is orchestrated by **Apache Airflow** running on EC2, with automatic retries, error notifications, and comprehensive logging.

## 📊 Data Storage Details

### Bronze Layer
- **Format:** JSON (raw API responses)
- **Location:** `s3://brewery-data-lake-bronze/`
- **Purpose:** Disaster recovery and reprocessing capability

### Silver Layer
- **Format:** Parquet (columnar, compressed)
- **Partitioning:** By `brewery_location` (e.g., `us/california/`)
- **Location:** `s3://brewery-data-lake-silver/`
- **Purpose:** Cleaned, standardized data ready for analytics

### Gold Layer
- **Format:** Apache Iceberg (ACID transactions, schema evolution, time travel)
- **Partitioning:** By `brewery_location`
- **Location:** `s3://brewery-data-lake-gold/`
- **Table:** `tb_ft_breweries_agg`
- **Purpose:** Business-ready aggregated metrics

## 🔨 Built With

| Component | Technology |
|-----------|-----------|
| **Cloud Platform** | Amazon Web Services (AWS) |
| **Data Ingestion** | AWS Lambda, Python |
| **Data Processing** | AWS Glue, PySpark |
| **Data Storage** | Amazon S3, Apache Parquet, Apache Iceberg |
| **Query Engine** | Amazon Athena (Serverless SQL) |
| **Orchestration** | Apache Airflow (EC2) |
| **Dashboard** | Streamlit (EC2) |
| **Monitoring** | Amazon CloudWatch |
| **Messaging** | AWS SNS, SES |
| **Infrastructure** | Docker, Docker Compose, EC2 |

## 📚 Documentation

For deeper dives into specific areas:

- **[Architecture](docs/architecture.md)** – Medallion pattern details, security model, data flow
- **[Airflow Orchestration](docs/airflow.md)** – DAG structure, task dependencies, scheduling
- **[AWS Infrastructure](docs/aws_setup.md)** – Services, IAM policies, and configuration
- **[Dashboard Guide](docs/dashboard.md)** – How to use the Streamlit application
- **[Monitoring & Alerting](docs/monitoring.md)** – CloudWatch metrics, health checks, incident response

## 📖 Code Structure

The codebase is organized by layer and function:

```
bws-breweries-pipeline/
├── aws/
│   ├── lambda_scripts/
│   │   ├── BronzeApiCaptureBreweries.py   # API ingestion
│   │   └── CleanFolder.py                  # S3 cleanup
│   ├── glue_scripts/
│   │   ├── bronze_to_silver.py            # Cleaning & standardization
│   │   └── silver_to_gold.py              # Aggregation
│   └── modules/
│       ├── logs.py          # CloudWatch logging
│       ├── quality.py       # Data quality checks
│       ├── pyspark_utils.py # PySpark helpers
│       └── utils.py         # AWS utilities
├── dags/
│   └── brewery_pipeline.py   # Airflow DAG definition
├── streamlit_app/
│   ├── main.py              # Dashboard application
│   ├── gold_analytics.py    # Analytics queries
│   ├── logs_observability.py # Monitoring section
│   ├── data_quality.py      # Quality checks display
│   └── utils/               # Database connectors, services
├── docker/
│   ├── docker-compose.yml   # Multi-service orchestration
│   └── docker.env           # Environment variables
├── docs/                    # Complete documentation
├── Makefile                 # Development commands
└── README.md                # This file
```

See the [AWS Setup Guide](docs/aws_setup.md) for details on each script and configuration.

## 🔒 Security

- **Read-only IAM user** – Safe exploration without production impact
- **S3 encryption at rest** – All data encrypted with AWS KMS
- **Audit logging** – CloudWatch logs all API calls and data access
- **Secrets management** – AWS Secrets Manager for API keys and credentials
- **No hardcoded secrets** – All credentials loaded from IAM roles or Secrets Manager
- **VPC isolation** – EC2 instances run in private VPC with restricted access

## 🚀 What's Happening in the Cloud

When you use this project, here's what's running on AWS:

**Serverless Components (Pay per use):**
- AWS Lambda – API ingestion (daily)
- AWS Glue – Data transformation (daily)
- AWS Athena – SQL queries (on-demand)
- Amazon S3 – Object storage (continuous)

**EC2 Components (Running 24/7):**
- Apache Airflow – Orchestration and scheduling
- Streamlit Dashboard – Web interface for analytics

All other services (CloudWatch, SNS, SES, Secrets Manager) are managed by AWS.

## 🤝 Getting Started

**New to this project?** Follow these steps:

1. ✅ Open the [live dashboard](http://56.124.50.116:8501/)
2. 📊 Explore brewery data with filters and visualizations
3. 📈 Check the Observability tab to see real-time pipeline health
4. 🔗 Access the data lake directly via AWS Console (read-only credentials above)
5. 📖 Read the [Architecture guide](docs/architecture.md) for a deeper understanding
6. 💻 Review the source code in `/aws`, `/dags`, and `/streamlit_app`

## ⚠️ Important Notes

- **Fully cloud-native** – Lambda, Glue, Athena, S3 all run on AWS infrastructure
- **EC2 only for dashboarding** – Streamlit and Airflow UI run on EC2 for accessibility
- **Automated scheduling** – Airflow triggers pipeline daily; no manual intervention needed
- **Error handling** – Automatic retries for transient failures; alerts sent on critical errors
- **Data quality checks** – Every layer includes validation; bad data is quarantined
- **Cost optimized** – Serverless architecture means you pay only for what you use

## 📞 Stay Connected

**Questions or feedback?**

- 📧 **Email:** brun0ws@outlook.com
- 💼 **LinkedIn:** [bruno-wds](https://www.linkedin.com/in/brunowds/)
- 📱 **WhatsApp:** +55 15 99759-5138

---

**Ready to explore?** [→ Open the Dashboard](http://56.124.50.116:8501/)

For technical questions, check the [docs](docs/) folder or review the CloudWatch logs in your AWS Console.
