# AWS Breweries Data Pipeline & Dashboard

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![AWS](https://img.shields.io/badge/AWS-Athena-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

Comprehensive data pipeline and interactive dashboard for brewery data aggregation using Apache Airflow, AWS Lambda, AWS Athena, and Streamlit.

## 📋 Overview

This project consists of two main components:

### 1. **Data Pipeline** (Airflow + AWS Lambda)
- Orchestrates daily data ingestion from Open Brewery API
- Stores raw data in S3 Bronze layer
- Scheduled pipeline with automatic retries and error handling
- Built with Apache Airflow 2.10.3

### 2. **Interactive Dashboard** (Streamlit)
- Web-based interface for querying brewery data
- Direct connection to AWS Athena
- Real-time data visualization and statistics
- Multi-format data export (CSV, JSON, Parquet)

---

## 🚀 Quick Start

### Quick Start - Dashboard Only

```bash
# 1. Clone and navigate
cd bws-breweries-pipeline

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure AWS (if not already done)
aws configure

# 5. Run the dashboard
streamlit run streamlit_app/main.py
```

Your dashboard will be available at: **http://localhost:8501**

### Quick Start Using Makefile

```bash
make venv
make install
make run
```

---

## 📁 Project Structure

```
bws-breweries-pipeline/
│
├── streamlit_app/                    # 📊 Interactive Dashboard
│   ├── main.py                      # Main Streamlit app
│   ├── config.py                    # Configuration settings
│   ├── utils/
│   │   ├── athena_connector.py     # AWS Athena connection
│   │   └── data_processing.py      # Data utilities
│   └── .streamlit/
│       ├── config.toml             # Streamlit UI config
│       └── secrets.toml.example    # Secrets template
│
├── dags/                            # 🔀 Airflow DAGs
│   └── brewery_pipeline.py         # Main pipeline definition
│
├── docker/                          # 🐳 Docker Configuration
│   ├── docker-compose.yml          # Docker services
│   └── docker.env                  # Environment variables
│
├── docs/                            # 📚 Documentation
│
├── requirements.txt                 # Python dependencies
├── Makefile                         # Development commands
├── .gitignore                       # Git ignore rules
├── STREAMLIT_README.md              # Full dashboard docs
├── SETUP_GUIDE_PT.md                # Setup guide (Portuguese)
└── README.md                        # This file
```

---

## 🔧 Configuration

### AWS Setup

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
