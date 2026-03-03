# Breweries Dashboard

## Overview

**Breweries Dashboard** is an interactive web application built with Streamlit that allows you to explore and analyze brewery aggregation data stored in AWS Athena. It provides a user-friendly interface for querying data, visualizing results, and exporting datasets in multiple formats.

### Features

- 🔍 **Interactive SQL Query Editor** - Write and execute custom SQL queries
- 📊 **Data Statistics** - View comprehensive data summaries and analytics
- 📥 **Multi-format Export** - Download results as CSV, JSON, or Parquet
- 🎯 **Sample Queries** - Quick access to pre-built queries
- ⚡ **Responsive UI** - Wide layout for better data visualization
- 🔐 **AWS Integration** - Secure connection to AWS Athena via configured credentials
- 📈 **Performance Metrics** - Track query execution and data insights

---

## Architecture

### Project Structure

```
streamlit_app/
├── main.py                          # Main Streamlit application entry point
├── config.py                        # Configuration constants and settings
├── utils/
│   ├── __init__.py                 # Package initialization
│   ├── athena_connector.py         # AWS Athena connection handler
│   └── data_processing.py          # Data transformation utilities
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
└── assets/                         # Images, logos, and static files
```

### Components

#### 1. **AthenaConnector** (`utils/athena_connector.py`)
Handles all interactions with AWS Athena:
- Query execution and monitoring
- Result retrieval and pagination
- Connection health checks
- Error handling and logging

#### 2. **DataProcessor** (`utils/data_processing.py`)
Provides data transformation utilities:
- Type conversion
- Data cleaning and deduplication
- Missing value handling
- Aggregations and filtering

#### 3. **Main Application** (`main.py`)
Streamlit UI components:
- Header and sidebar
- Query editor
- Results display
- Statistics visualization
- Export functionality

---

## Prerequisites

- Python 3.9+
- AWS credentials configured locally (via `~/.aws/credentials` or environment variables)
- Access to AWS Athena with the `gold` database
- Internet connection for AWS API calls

---

## Installation

### 1. Clone the repository

```bash
cd bws-breweries-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AWS Credentials

Ensure your AWS credentials are configured. You can do this in multiple ways:

**Option A: Using AWS CLI**
```bash
aws configure
```

**Option B: Using environment variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=sa-east-1
```

**Option C: Using credentials file**
Create `~/.aws/credentials`:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

---

## Configuration

### Application Settings

Edit `config.py` to customize:

```python
# AWS Configuration
AWS_REGION = "sa-east-1"
ATHENA_DATABASE = "gold"
ATHENA_TABLE = "tb_ft_breweries_agg"
ATHENA_S3_OUTPUT = "s3://bws-dl-logs-sae1-prd/athena/query_results/"

# UI Settings
DEFAULT_ROWS_TO_DISPLAY = 1000
STREAMLIT_LAYOUT = "wide"
```

### Streamlit Configuration

Modify `.streamlit/config.toml` for theme, header, and behavior customization.

---

## Usage

### 1. Start the Dashboard

```bash
streamlit run streamlit_app/main.py
```

The application will open in your default browser at `http://localhost:8501`

### 2. Execute Queries

**Using Query Editor:**
1. Enter your SQL query in the text area
2. Click "▶️ Run Query"
3. View results in the table below

**Using Sample Queries:**
1. Select a sample query from the sidebar dropdown
2. Query automatically populates in the editor
3. Click "▶️ Run Query"

### 3. Analyze Results

- View data in interactive table
- Check data statistics (summary, missing values, unique counts)
- Download results in your preferred format

### 4. Export Data

Click any of these buttons to download:
- 📥 **Download CSV** - Comma-separated values
- 📥 **Download JSON** - JSON format
- 📥 **Download Parquet** - Apache Parquet format

---

## Query Examples

### Find Top 10 Breweries by Count

```sql
SELECT
    brewery_name,
    COUNT(*) as total_count
FROM gold.tb_ft_breweries_agg
GROUP BY brewery_name
ORDER BY total_count DESC
LIMIT 10
```

### Breweries by State

```sql
SELECT
    state,
    COUNT(DISTINCT brewery_id) as brewery_count,
    COUNT(*) as total_records
FROM gold.tb_ft_breweries_agg
GROUP BY state
ORDER BY total_records DESC
```

### Breweries with Recent Updates

```sql
SELECT *
FROM gold.tb_ft_breweries_agg
WHERE last_updated IS NOT NULL
ORDER BY last_updated DESC
LIMIT 100
```

---

## Troubleshooting

### Error: "Failed to connect to AWS Athena"

**Solution:**
- Verify AWS credentials are configured
- Check IAM permissions for Athena access
- Ensure correct region is specified

```bash
# Test AWS connection
aws sts get-caller-identity
```

### Error: "Query execution timeout"

**Solution:**
- Reduce rows in LIMIT clause
- Add WHERE filters to narrow results
- Check Athena query performance

### Error: "Table not found"

**Solution:**
- Verify table name: `gold.tb_ft_breweries_agg`
- Check database permissions
- Confirm Athena role has access to the S3 location

### Slow Performance

**Optimization Tips:**
- Use LIMIT to reduce result set size
- Add WHERE clauses to filter data
- Use materialized views for frequent queries
- Format S3 data with proper partitioning

---

## Development

### Project Dependencies

- **streamlit** - Web application framework
- **boto3** - AWS SDK
- **pandas** - Data manipulation
- **pyarrow** - Parquet support

### Adding New Features

1. **Add utility functions** in `utils/data_processing.py`
2. **Update configuration** in `config.py`
3. **Implement UI components** in `main.py`
4. **Test thoroughly** before deployment

### Code Style

- Follow PEP 8 style guide
- Use descriptive variable names
- Add docstrings to functions
- Include type hints where applicable

---

## Security Considerations

⚠️ **Important:**

1. **Credentials Management**
   - Never commit AWS credentials to version control
   - Use IAM roles when running in AWS environments
   - Rotate credentials regularly

2. **Data Access**
   - Implement row-level security in Athena views if needed
   - Use least-privilege IAM policies
   - Monitor query costs and access logs

3. **Application Deployment**
   - Use HTTPS for production deployments
   - Implement authentication/authorization
   - Run Streamlit behind a reverse proxy (nginx, etc.)

---

## Performance Optimization

### Athena Query Best Practices

1. **Partition Pruning** - Use WHERE clauses on partitioned columns
2. **Column Selection** - SELECT only needed columns
3. **Data Format** - Use Parquet or ORC for better compression
4. **Result Size** - Limit results to necessary rows

### Application Caching

The application caches Athena connector instance:
```python
@st.cache_resource
def get_athena_connector():
    return AthenaConnector()
```

Clear cache using the "🗑️ Clear Cache" button in the sidebar.

---

## Logging

Logs are written to console. Adjust logging level in `config.py`:

```python
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## Support & Documentation

### Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [AWS Athena Documentation](https://docs.aws.amazon.com/athena/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Common Questions

**Q: Can I schedule queries?**
A: Currently not supported. Queries run on-demand. Consider AWS Athena Workgroups for scheduled queries.

**Q: How much does Athena cost?**
A: Athena charges per GB scanned. Optimize queries to minimize scanned data.

**Q: Can I connect to other databases?**
A: Yes, but requires code changes. Create new connector classes in `utils/`.

---

## Version History

### v1.0.0 (2026-03-02)

- Initial release
- Core query execution functionality
- Data statistics and export
- Sample queries
- Multi-format export (CSV, JSON, Parquet)

---

## License

This project is proprietary and confidential.

---

## Author

Data Team
Version: 1.0.0
Last Updated: 2026-03-02

---

## Changelog

### Planned Features

- [ ] Query history and favorites
- [ ] Data visualization (charts, maps)
- [ ] Scheduled query reports
- [ ] User authentication
- [ ] Query optimization suggestions
- [ ] Real-time data monitoring
