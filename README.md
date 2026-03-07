# AWS Breweries Data Lake & Analytics Platform

![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-623CE4?style=for-the-badge&logo=terraform&logoColor=white)

A comprehensive data lake architecture built on AWS, implementing the Medallion Architecture pattern for brewery data analytics. This project showcases modern data engineering practices with automated pipelines, real-time monitoring, and interactive dashboards.

## 🏗️ Architecture

Our data lake follows the Medallion Architecture, processing data through Bronze, Silver, and Gold layers for optimal analytics performance.

<iframe width="768" height="496" src="https://miro.com/app/live-embed/uXjVG24Xf7s=/?focusWidget=3458764662592067466&embedMode=view_only_without_ui&embedId=571479114836" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>

For detailed architecture documentation, see [docs/architecture.md](docs/architecture.md).

## 📊 Data Pipeline Overview

The pipeline orchestrates end-to-end data processing from API ingestion to analytics-ready datasets:

1. **API Ingestion**: Lambda functions collect brewery data from external APIs
2. **Bronze Layer**: Raw data storage with initial validation
3. **Silver Layer**: Cleaned and standardized data
4. **Gold Layer**: Business-ready datasets optimized for analytics
5. **Quality Checks**: Automated validation and monitoring
6. **Consumption**: Multiple interfaces for data access

## 🏛️ Medallion Architecture

### Bronze Layer (Raw)
- Raw, unprocessed data from source systems
- Minimal transformations applied
- Preserves original data fidelity
- Used for data recovery and reprocessing

### Silver Layer (Cleaned)
- Standardized schemas and data types
- Basic data quality validations
- Deduplication and null handling
- Ready for downstream processing

### Gold Layer (Curated)
- Business-rule compliant datasets
- Optimized for query performance
- Aggregated metrics and KPIs
- Direct consumption by analytics tools

## 🔄 Airflow Orchestration

Pipeline orchestration is managed through Apache Airflow with a comprehensive DAG that handles:

- API data ingestion via Lambda
- Multi-layer data transformations with Glue
- Automated data quality validations
- Comprehensive monitoring and alerting

![Airflow DAG](docs/images/airflow_dag.png)

For complete Airflow documentation, see [docs/airflow.md](docs/airflow.md).

## 📈 Streamlit Dashboard

An interactive web application providing three analytical perspectives:

### Analytics Tab
Explore brewery data with interactive filters, visualizations, and export capabilities.

### Observability Tab
Real-time monitoring of pipeline health, performance metrics, and system status.

### Data Quality Tab
Comprehensive data quality monitoring with validation rules and quality reports.

**Demo Videos:**
- [Analytics Demo](docs/videos/analytics.mp4)
- [Observability Demo](docs/videos/observability.mp4)
- [Data Quality Demo](docs/videos/data_quality.mp4)

For detailed dashboard documentation, see [docs/dashboard.md](docs/dashboard.md).

## 📁 Repository Structure

```
bws-breweries-pipeline/
│
├── streamlit_app/                    # 📊 Interactive Dashboard
│   ├── main.py                      # Main Streamlit application
│   ├── config.py                    # Configuration settings
│   ├── utils/                       # Utility modules
│   │   ├── athena_connector.py     # AWS Athena connection
│   │   ├── data_processing.py      # Data processing utilities
│   │   └── analytics_service.py    # Analytics functions
│   └── Dockerfile                   # Container configuration
│
├── dags/                            # 🔀 Airflow Orchestration
│   └── brewery_pipeline.py         # Main pipeline DAG
│
├── docker/                          # 🐳 Docker Configuration
│   ├── docker-compose.yml          # Multi-service setup
│   └── docker.env                  # Environment variables
│
├── docs/                            # 📚 Documentation
│   ├── architecture.md             # Architecture details
│   ├── airflow.md                  # Airflow orchestration
│   ├── aws_setup.md                # AWS infrastructure
│   ├── dashboard.md                # Dashboard guide
│   ├── images/                     # Architecture diagrams
│   └── videos/                     # Demo videos
│
├── requirements.txt                 # Python dependencies
├── Makefile                         # Development commands
└── README.md                        # This file
```

## ☁️ AWS Infrastructure

The project leverages multiple AWS services for a complete data lake solution:

- **Lambda**: Serverless API ingestion
- **S3**: Multi-tier data storage (Bronze/Silver/Gold)
- **Glue**: ETL processing and catalog management
- **Athena**: Serverless SQL queries
- **DynamoDB**: Metadata and configuration storage
- **CloudWatch**: Monitoring and alerting
- **SES**: Email notifications

For detailed AWS setup and configuration, see [docs/aws_setup.md](docs/aws_setup.md).

## 🔐 Security & Read-only Access

This project includes a read-only IAM user configuration for safe exploration and demonstration. The read-only user provides:

- **S3 Read Access**: Browse Bronze, Silver, and Gold layer data
- **Athena Query Access**: Execute SQL queries on processed datasets
- **Glue Catalog Access**: Explore table schemas and metadata

This setup ensures stakeholders can analyze data without risking production integrity, perfect for portfolio demonstrations and collaborative exploration.

## 📊 Observability & Logging

Comprehensive monitoring across all pipeline components:

- **CloudWatch Metrics**: Performance monitoring and custom dashboards
- **Structured Logging**: Application-level logs with context
- **Alert Management**: Automated notifications for pipeline issues
- **Health Checks**: Real-time system status and data quality metrics
- **Audit Trails**: Complete audit logging for compliance

## 👨‍💻 About the Author

**Bruno William**

*Data Engineer specializing in AWS Data Platforms*

**Skills:**
- AWS (Lambda, S3, Glue, Athena, CloudWatch)
- Python & PySpark for data processing
- Apache Airflow for workflow orchestration
- Streamlit for interactive dashboards
- Terraform for infrastructure as code

**Connect:**
- GitHub: [brunobws](https://github.com/brunobws)
- LinkedIn: [Coming Soon]

## 🗺️ Roadmap

- [ ] **Infrastructure as Code**: Complete Terraform implementation
- [ ] **CI/CD Pipeline**: Automated testing and deployment
- [ ] **Data Quality Framework**: Advanced validation and anomaly detection
- [ ] **Dashboard Enhancements**: Additional analytics and visualization features
- [ ] **Observability Expansion**: Advanced monitoring and alerting capabilities

## 🛠️ Technologies Used

- **Cloud Platform**: Amazon Web Services (AWS)
- **Data Processing**: Python, PySpark, AWS Glue
- **Orchestration**: Apache Airflow
- **Storage**: Amazon S3, DynamoDB
- **Analytics**: Amazon Athena
- **Dashboard**: Streamlit
- **Monitoring**: Amazon CloudWatch
- **Containerization**: Docker, Docker Compose
- **Infrastructure**: Terraform (planned)

## 🎯 Project Goal

This project demonstrates enterprise-grade data engineering capabilities on AWS, showcasing:

- Scalable data lake architecture with Medallion pattern
- Automated ETL pipelines with comprehensive monitoring
- Interactive analytics dashboards for business users
- Production-ready security and access controls
- Complete documentation and professional presentation

Perfect for portfolio demonstration and real-world data platform implementation.

**Ensure you have:**
- AWS Account with Athena access
- IAM credentials configured
- Access to S3 location: `s3://bws-dl-logs-sae1-prd/athena/query_results/`
- Database `gold` in Athena with table `tb_ft_breweries_agg`

**Configure credentials:**

```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=sa-east-1
```

### Dashboard Configuration

Edit `streamlit_app/config.py`:

```python
# AWS settings
ATHENA_DATABASE = "gold"
ATHENA_TABLE = "tb_ft_breweries_agg"
ATHENA_S3_OUTPUT = "s3://bws-dl-logs-sae1-prd/athena/query_results/"

# UI settings
DEFAULT_ROWS_TO_DISPLAY = 1000
STREAMLIT_LAYOUT = "wide"
```

---

## 📊 Using the Dashboard

### 1. Start the Application

```bash
streamlit run streamlit_app/main.py
```

### 2. Query Data

Choose one of these methods:

**Method A: Write Custom SQL**
```sql
SELECT brewery_name, COUNT(*) as count
FROM gold.tb_ft_breweries_agg
GROUP BY brewery_name
ORDER BY count DESC
LIMIT 20
```

**Method B: Use Sample Queries**
- Select from dropdown in sidebar
- Auto-populated sample queries included

### 3. Analyze Results

- View data in interactive table
- Check statistics panel
- Download in multiple formats

### 4. Export Data

Available formats:
- 📄 **CSV** - For spreadsheets
- 📋 **JSON** - For APIs
- 📦 **Parquet** - For data warehouses

---

## 🔄 Pipeline Overview

### Data Flow

```
Open Brewery API
      ↓
AWS Lambda (BronzeApiCaptureBreweries)
      ↓
S3 Bronze Layer (Raw Data)
      ↓
AWS Glue (Transform & Aggregate)
      ↓
S3 Gold Layer (Gold Table)
      ↓
AWS Athena (Query Layer)
      ↓
Streamlit Dashboard (Visualization)
```

### Airflow DAG Execution

- **Schedule**: Daily at midnight
- **Owner**: bruno
- **Retries**: 2 attempts
- **Database**: PostgreSQL (in Docker)
- **Webserver**: Available at `http://localhost:8080`

---

## 🐳 Docker Services

The project includes Docker Compose for local development:

```bash
# Start services
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

**Services:**
- **PostgreSQL** - Airflow metadata database
- **Airflow Webserver** - UI at `http://localhost:8080`
- **Airflow Scheduler** - Runs DAGs

---

## 📝 Code Quality

Format and lint code:

```bash
# Format with Black
make format

# Lint with Flake8
make lint

# Or manual
black streamlit_app/
flake8 streamlit_app/
```

---

## 🚨 Troubleshooting

### Error: "Failed to connect to AWS Athena"

```bash
# Verify AWS credentials
aws sts get-caller-identity

# Check AWS configuration
aws configure list
```

### Error: "Table not found"

```bash
# Verify table exists
aws athena start-query-execution \
  --query-string "SELECT * FROM gold.tb_ft_breweries_agg LIMIT 1" \
  --result-configuration OutputLocation=s3://bws-dl-logs-sae1-prd/athena/query_results/
```

### Slow Query Performance

- Add `LIMIT` to queries
- Use `WHERE` clauses to filter
- Select only needed columns
- Avoid complex JOINs

---

## 📚 Documentation

- **[Streamlit Dashboard Docs](./STREAMLIT_README.md)** - Complete dashboard documentation
- **[Setup Guide (PT)](./SETUP_GUIDE_PT.md)** - Portuguese setup instructions
- **[Airflow DAG](./dags/brewery_pipeline.py)** - Pipeline code
- **[AWS Athena Docs](https://docs.aws.amazon.com/athena/)** - AWS documentation

---

## 🔐 Security

⚠️ **Important Security Notes:**

1. **Never commit credentials**
   ```bash
   # .gitignore includes:
   .aws/
   .env
   secrets.toml
   ```

2. **Use IAM Roles in Production**
   - Avoid hardcoding credentials
   - Use instance profiles for EC2/ECS

3. **Implement Authentication for Shared Deployments**
   - Use Streamlit Cloud authentication
   - Add reverse proxy (nginx) with auth

4. **Restrict IAM Permissions**
   - Use least-privilege policies
   - Limit Athena access to specific databases/tables

---

## 📦 Dependencies

### Core
- `streamlit` - Web framework
- `boto3` - AWS SDK
- `pandas` - Data manipulation
- `pyarrow` - Parquet support

### Pipeline
- `apache-airflow` - Orchestration
- `apache-airflow-providers-amazon` - AWS integration

### Development
- `black` - Code formatting
- `flake8` - Linting

Full list: See `requirements.txt`

---

## 🛠️ Development Workflow

### 1. Setup

```bash
make dev-install
make aws-check
```

### 2. Make Changes

Edit files in `streamlit_app/`

### 3. Format and Lint

```bash
make format
make lint
```

### 4. Run

```bash
make run
```

---

## 🤝 Contributing

1. Create a feature branch
2. Make changes following code style guide
3. Run linting
4. Commit with descriptive messages
5. Push and create pull request

---

## 📈 Performance Tips

- **Queries**: Add `LIMIT` and `WHERE` clauses
- **Caching**: Streamlit caches connector and data automatically
- **S3**: Partition data by date or region
- **Athena**: Use partitioned queries to reduce scanned data

---

## 📞 Support

### Common Issues

| Issue | Solution |
|-------|----------|
| AWS connection fails | Run `aws configure` |
| Slow queries | Add LIMIT and WHERE |
| Module not found | Activate venv, run `pip install -r requirements.txt` |
| Port 8501 in use | `streamlit run ... --server.port 8502` |

### Contact

- **Documentation**: See `STREAMLIT_README.md`
- **Setup Help**: See `SETUP_GUIDE_PT.md`

---

## 📄 License

Proprietary - Confidential

---

## 👥 Authors

**Data Team**

- Version: 1.0.0
- Last Updated: March 2, 2026
- Repository: `bws-breweries-pipeline`

---

## 🗂️ Changelog

### v1.0.0 (2026-03-02)
- ✅ Initial release
- ✅ Streamlit dashboard implementation
- ✅ Athena connector with full query support
- ✅ Data processing utilities
- ✅ Multi-format export (CSV, JSON, Parquet)
- ✅ Sample queries and statistics
- ✅ Comprehensive documentation

### Planned Features
- 🔜 Query history and favorites
- 🔜 Data visualization (charts, maps)
- 🔜 Scheduled reports
- 🔜 User authentication
- 🔜 Query performance optimization suggestions

---

## 🔗 Related Documents

- [Full Streamlit Documentation](./STREAMLIT_README.md)
- [Setup Guide (Portuguese)](./SETUP_GUIDE_PT.md)
- [Airflow Configuration](./dags/brewery_pipeline.py)
- [Docker Configuration](./docker/docker-compose.yml)

---

**Happy data exploring! 🍺📊**
