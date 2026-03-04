# Data Platform Monitoring & Analytics Dashboard

## 🚀 Overview

A production-ready Streamlit dashboard for the AWS Medallion Data Lake that transforms raw operational data into actionable insights. Monitor pipeline health, analyze brewery distributions, and track data quality metrics all in one place.

**Version:** 2.0.0  
**Last Updated:** 2026-03-04

---

## ✨ Features

### 📊 Tab 1: Gold Analytics
- **Interactive Brewery Analytics** - Explore aggregated brewery data by country, state, and type
- **Multi-Dimensional Filters** - Filter by country, state, and brewery type with multiselect dropdowns
- **Real-Time KPIs** - Display total breweries, countries, states, and types
- **Data Visualizations**
  - Bar chart: Breweries by type
  - Horizontal bar chart: Top 10 states
- **Sortable Data Table** - Detailed view with export options
- **Multi-Format Export** - Download as CSV, JSON, or Parquet

### 📈 Tab 2: Logs Observability
- **Pipeline Health Monitoring** - Real-time execution logs and status tracking
- **Advanced Filtering** - Filter by layer, job name, status, and date range
- **Comprehensive KPIs**
  - Total executions count
  - Success rate percentage
  - Error and warning counts
  - Average execution duration
- **Visual Analytics**
  - Line chart: Daily execution trends
  - Pie chart: Execution status distribution
  - Bar chart: Average duration by job
  - Bar chart: Executions per layer
- **Recent Activity Table** - Latest executions with sortable columns
- **Data Export** - CSV and JSON downloads

### 🧪 Tab 3: Data Quality Dashboard
- **BDQ (Business Data Quality) Monitoring** - Track data quality test results
- **Critical Insights**
  - % executions with BDQ enabled
  - % critical tables
  - Critical table failures
  - Warning trends over time
- **DQ Test Analytics**
  - Most common test failures by column
  - Test type distribution pie chart
  - 30-day warning trends
  - Critical table health status
- **Test Result Details** - Recent failures with column, test type, and error information
- **JSON Parser Integration** - Automatically parses and normalizes the "info" field containing DQ test metadata

---

## 🏗️ Architecture

### Project Structure

```
streamlit_app/
├── main.py                          # Main dashboard entry point with tabs
├── config.py                        # Centralized configuration & constants
├── gold_analytics.py                # Tab 1: Analytics page
├── logs_observability.py            # Tab 2: Observability page
├── data_quality.py                  # Tab 3: Data Quality page
│
├── utils/
│   ├── __init__.py
│   ├── config.py                    # Configuration loader with env vars
│   ├── logger.py                    # Centralized logging setup
│   ├── cache_manager.py             # Streamlit caching utilities
│   ├── athena_service.py            # 🔧 FIXED Athena connector (critical!)
│   ├── parser_service.py            # JSON parsing for DQ info field
│   ├── analytics_service.py         # Data aggregation & KPI calculations
│   ├── data_processing.py           # Legacy data utilities (kept for compatibility)
│   └── athena_connector.py          # Legacy Athena connector (deprecated)
│
└── .streamlit/
    └── config.toml                  # Streamlit UI configuration
```

### Key Services

#### **AthenaService** (`utils/athena_service.py`) - THE BUG FIX 🔧
The critical fix for the original issue: **Properly waits for query completion before fetching results.**

Flow:
```
1. _submit_query()              → start_query_execution() → get execution_id
2. _wait_for_query_completion() → poll get_query_execution() until SUCCEEDED
3. _fetch_results()             → get_query_results() with pagination
4. execute_query()              → orchestrates all three steps → returns DataFrame
```

**What was fixed:**
- ✅ Proper async query handling with status polling
- ✅ Waits for SUCCEEDED state before fetching results (no race condition)
- ✅ Handles pagination for large result sets
- ✅ Comprehensive error handling for FAILED/CANCELLED states
- ✅ Logging at every step for debugging

#### **ParserService** (`utils/parser_service.py`)
Extracts and normalizes data quality test results from the JSON "info" field.

**Capabilities:**
- Parses JSON-like strings safely
- Normalizes DQ test results (column_tested, test_applied, status, timestamp)
- Extracts test metadata and results
- Identifies critical failures
- Counts executions by status

#### **AnalyticsService** (`utils/analytics_service.py`)
Business logic for aggregations and KPI calculations.

**Features:**
- KPI calculation with flexible operations (count, sum, avg, max, min, unique)
- Success rate computation
- Time series aggregation (daily, weekly, monthly)
- Top failures identification
- Percentile calculations
- Date range filtering

#### **CacheManager** (`utils/cache_manager.py`)
Streamlit session state caching with TTL.

- Decorator-based caching: `@cached_query(ttl_seconds=300)`
- Automatic expiration handling
- Configurable TTL per query
- Cache invalidation utilities

---

## 📋 Prerequisites

- **Python 3.9+**
- **AWS Credentials** configured locally (via `~/.aws/credentials` or environment variables)
- **AWS IAM Permissions:**
  - `athena:StartQueryExecution`
  - `athena:GetQueryExecution`
  - `athena:GetQueryResults`
  - `s3:GetObject` (for query result location)
- **Data in Athena:**
  - `gold.tb_ft_breweries_agg` table (Iceberg format)
  - `logs.execution_logs` table (Parquet format)

---

## 🔧 Installation & Setup

### 1. Clone Repository

```bash
cd bws-breweries-pipeline_2
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AWS Credentials

**Option A: Using AWS CLI**
```bash
aws configure
# Enter: Access Key, Secret Key, Region (sa-east-1), Output format (json)
```

**Option B: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=sa-east-1
```

**Option C: Credentials File**
Create `~/.aws/credentials`:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY

[default]
region = sa-east-1
```

### 5. Set Environment Variables (Optional)

```bash
export ATHENA_DATABASE=gold
export ATHENA_LOGS_DATABASE=logs
export ATHENA_S3_OUTPUT=s3://bws-dl-logs-sae1-prd/athena/query_results/
export LOG_LEVEL=INFO
```

### 6. Run the Dashboard

```bash
streamlit run streamlit_app/main.py
```

The app will open at `http://localhost:8501`

---

## 🎯 Data Tables

### Gold Table: `gold.tb_ft_breweries_agg`

Aggregated brewery counts by country, state, and type.

| Column | Type | Description |
|--------|------|-------------|
| `nm_country` | string | Country name |
| `nm_state` | string | State/Province name |
| `ds_brewery_type` | string | Type of brewery (Microbrewery, Macro, etc.) |
| `nr_total_breweries` | bigint | Count of breweries |

### Logs Table: `logs.execution_logs`

Pipeline execution logs with data quality metadata.

| Column | Type | Description |
|--------|------|-------------|
| `start_execution` | timestamp | When execution started |
| `end_execution` | timestamp | When execution ended |
| `source` | string | Data source |
| `table_name` | string | Target table |
| `job_name` | string | Airflow DAG/task name |
| `status` | string | SUCCEEDED, FAILED, RUNNING, CANCELLED |
| `error` | string | Error message if failed |
| `layer` | string | Data layer (bronze, silver, gold, quality) |
| `error_description` | string | Detailed error text |
| `warning_description` | string | Warnings if any |
| `has_bdq` | boolean | Data quality tests enabled |
| `critical_table` | boolean | Is this a critical table |
| `file_name` | string | Source file path |
| `count` | bigint | Rows processed |
| `info` | string | **JSON** - Data Quality test results (parsed by ParserService) |
| `dt_ref` | date | Partition key (date reference) |

**The "info" Column:** Contains JSON-like test results. Example:
```json
{
  "column": "customer_id",
  "test_type": "uniqueness",
  "status": "PASSED",
  "timestamp": "2026-03-04T10:30:00Z",
  "threshold": 100.0,
  "value": 99.8
}
```

---

## 📊 Usage Guide

### Tab 1: Gold Analytics

1. **Load Data** - Click any filter to populate available options
2. **Filter Results** - Use multiselect dropdowns to filter countries, states, brewery types
3. **View KPIs** - See real-time counts updated based on filters
4. **Analyze Charts** - Hover over charts for details
5. **Export Data** - Download filtered results in preferred format

### Tab 2: Logs Observability

1. **Select Filters** - Choose specific layers, jobs, and statuses
2. **Monitor Health** - Check success rate and error counts
3. **Identify Trends** - View execution patterns over time
4. **Drill Down** - Click on recent execution table for details
5. **Track Performance** - Monitor average execution duration

### Tab 3: Data Quality

1. **Enable BDQ Filter** - Toggle to show only BDQ-enabled executions
2. **Focus on Critical** - Filter to critical tables only if needed
3. **Analyze Failures** - Identify most common failing columns and tests
4. **Track Trends** - See warning patterns over 30 days
5. **Review Details** - Examine recent test failures

---

## 🔄 How Athena Query Execution Works (FIXED)

### The Bug & The Fix

**Original Problem:**
```python
# ❌ WRONG - Executes query but returns immediately, before results are ready
execution_id = client.start_query_execution(...)
results = client.get_query_results(execution_id)  # Query still running!
```

**Fixed Implementation:**
```python
# ✅ CORRECT - Waits for completion, then fetches results
execution_id = self._submit_query(query, database)           # Step 1: Start
self._wait_for_query_completion(execution_id)                # Step 2: Poll until SUCCEEDED
df = self._fetch_results(execution_id)                       # Step 3: Get results
```

### Query Flow Diagram

```
User clicks "Run Query"
          ↓
execute_query(sql_string)
          ↓
_submit_query()
  └─ start_query_execution()
  └─ returns execution_id
          ↓
_wait_for_query_completion()  ← THE FIX
  └─ Loop {
      └─ get_query_execution() → check Status.State
      └─ if SUCCEEDED → break ✅
      └─ if FAILED/CANCELLED → raise Error ❌
      └─ else → sleep(1) and retry
      └─ timeout after 5 minutes
    }
          ↓
_fetch_results()
  └─ get_paginator("get_query_results")
  └─ iterate pages
  └─ extract rows and columns
  └─ build DataFrame
          ↓
return DataFrame → Display in UI ✅
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# AWS Settings
AWS_REGION=sa-east-1                                      # AWS region
ATHENA_DATABASE=gold                                      # Gold database name
ATHENA_LOGS_DATABASE=logs                                 # Logs database name
ATHENA_S3_OUTPUT=s3://bws-dl-logs-sae1-prd/...          # Query result location

# Application Settings
LOG_LEVEL=INFO                                            # DEBUG, INFO, WARNING, ERROR
CACHE_TTL=300                                             # Cache expiry in seconds
```

### Streamlit Config (`~/.streamlit/config.toml`)

Already configured with:
- **Theme:** Light mode with professional colors
- **Layout:** Wide (better for data viz)
- **Error Details:** Enabled for debugging
- **CORS:** Disabled for security
- **Stats:** Disabled (privacy)

---

## 🧪 Testing & Validation

### Test Athena Connection

```python
from utils.athena_service import AthenaService

service = AthenaService()
is_healthy = service.health_check()
print(f"Athena accessible: {is_healthy}")
```

### Test Query Execution

```python
query = """
SELECT COUNT(*) as total
FROM gold.tb_ft_breweries_agg
"""

df = service.query_gold(query)
print(df)
```

### Test Data Quality Parsing

```python
from utils.parser_service import ParserService

info_json = '{"column": "id", "test_type": "uniqueness", "status": "PASSED"}'
result = ParserService.normalize_dq_info(info_json)
print(result)
```

---

## 📈 Performance Optimization

### Best Practices

1. **Partition Pruning** - Use WHERE conditions on `dt_ref` column
2. **Column Selection** - Only SELECT needed columns
3. **Result Limits** - Use LIMIT to reduce data transfer
4. **Caching** - Results cached for 5 minutes by default
5. **Async Polling** - Don't block UI, poll in background

### Query Optimization Examples

```sql
-- ✅ GOOD: Partition pruned, limited columns, row limit
SELECT nm_country, nm_state, nr_total_breweries
FROM gold.tb_ft_breweries_agg
WHERE nm_country IN ('USA', 'Canada')
LIMIT 1000

-- ❌ AVOID: Full scan, unnecessary columns
SELECT * FROM gold.tb_ft_breweries_agg
```

---

## 🚨 Troubleshooting

### "Connection Failed" Error

**Check AWS Credentials:**
```bash
aws sts get-caller-identity
```

Expected output shows your account ID. If not:
1. Reconfigure with `aws configure`
2. Check `~/.aws/credentials` file exists
3. Verify environment variables are set

### Query Timeout

**Solution:**
1. Add WHERE clause to filter data
2. Reduce LIMIT value
3. Select only needed columns
4. Check if table is partitioned correctly

### No Results Returned

**The Original Bug - Now Fixed!**
- ✅ Our `AthenaService` properly waits for query completion
- ✅ Results are fetched after status = SUCCEEDED
- ✅ All data is returned to UI

If still no results:
1. Check table exists: `SHOW TABLES IN gold;`
2. Verify data: `SELECT COUNT(*) FROM gold.tb_ft_breweries_agg;`
3. Check query syntax in Athena console

### Slow Performance

1. Check S3 path configuration
2. Verify data is in Parquet/Iceberg format
3. Use EXPLAIN to analyze query plan
4. Consider materialized views for frequent queries

---

## 🔐 Security

### Best Practices

1. **Never commit credentials** to git
2. **Use IAM roles** in production (not access keys)
3. **Restrict IAM policies** to minimum required permissions
4. **Enable S3 encryption** for query results
5. **Use VPC endpoints** for private Athena access
6. **Rotate credentials** regularly
7. **Audit access logs** in CloudTrail

### IAM Policy Example

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AthenaFullAccess",
      "Effect": "Allow",
      "Action": [
        "athena:StartQueryExecution",
        "athena:GetQueryExecution",
        "athena:GetQueryResults",
        "athena:ListQueryExecutions"
      ],
      "Resource": "arn:aws:athena:sa-east-1:ACCOUNT_ID:workgroup/primary"
    },
    {
      "Sid": "S3AccessForQueryResults",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::bws-dl-logs-sae1-prd/athena/*"
    }
  ]
}
```

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [AWS Athena Documentation](https://docs.aws.amazon.com/athena/)
- [Boto3 Athena Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Express](https://plotly.com/python/plotly-express/)

---

## 📝 Development

### Adding a New Tab

1. Create new file: `streamlit_app/new_tab.py`
2. Implement `render_new_tab(athena_service)` function
3. Add import to `main.py`
4. Add tab in `st.tabs()` section
5. Test thoroughly

### Extending Services

- **Add analytics:** New method in `AnalyticsService`
- **Add parser logic:** New method in `ParserService`
- **Custom caching:** Use `@cached_query` decorator
- **New queries:** Add static query method to `AthenaService`

---

## 🤝 Support

For issues or questions:
1. Check CloudWatch logs for Athena errors
2. Review Athena query editor for query issues
3. Check IAM permissions
4. Verify table schema with `DESCRIBE TABLE`

---

## 📄 License

Proprietary and Confidential - Data Team 2026

---

## 👥 Contributors

- Data Team

---

## ✅ Changelog

### v2.0.0 (2026-03-04)
- ✅ **FIXED:** Athena query execution bug (proper wait mechanism)
- ✅ **NEW:** Production-ready modular architecture
- ✅ **NEW:** Three comprehensive tabs (Analytics, Observability, DQ)
- ✅ **NEW:** Data quality JSON parsing
- ✅ **NEW:** Advanced filtering and KPIs
- ✅ **NEW:** Professional visualizations
- ✅ **IMPROVED:** Error handling and logging
- ✅ **IMPROVED:** Caching with TTL

### v1.0.0 (2026-03-02)
- Initial dashboard with query editor
- Multi-format export (CSV, JSON, Parquet)
- Basic Athena connectivity (with bug)

---

**Status:** ✅ Production Ready | 🔧 Fully Tested | 📊 Feature Complete
