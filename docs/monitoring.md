# Monitoring & Alerting

This document describes the observability and alerting strategy for the brewery data pipeline.

## Overview

The pipeline implements comprehensive monitoring across all layers to ensure data quality, pipeline reliability, and rapid incident detection. We use **CloudWatch** for metrics and logs, combined with **Streamlit dashboards** for visualization and **SES** for email alerts.

## CloudWatch Monitoring

### Metrics

**Pipeline Execution Metrics:**
- `PipelineExecutionTime` – Duration of entire pipeline from ingestion to gold layer
- `LambdaInvocationTime` – API ingestion time
- `GlueJobDuration` (Bronze→Silver) – Data cleaning job duration
- `GlueJobDuration` (Silver→Gold) – Aggregation job duration
- `RecordsProcessed` – Count of records at each layer
- `DataQualityFailures` – Failed quality checks per run

**Data Quality Metrics:**
- `NullRecordCount` – Records with null values
- `DuplicateRecordCount` – Duplicate records detected
- `SchemaValidationFailures` – Records failing schema validation
- `OutlierRecordCount` – Records flagged as statistical outliers

**Infrastructure Metrics:**
- `S3BucketSize` – Data lake storage utilization
- `AthenaQueryCount` – Number of Athena queries executed
- `AthenaCostEstimate` – Estimated query costs
- `LambdaErrorRate` – API ingestion failures
- `GlueJobErrorRate` – ETL job failures

### Log Analysis

All pipeline components write to **CloudWatch Logs** in structured JSON format:

**Lambda Logs:**
- Request metadata (source, execution context)
- API response details (status, record count, pagination)
- Error traces and retry attempts
- Ingestion timestamps and S3 location confirmation

**Glue Job Logs:**
- Job start/end timestamps
- Records read, processed, written
- Schema transformations applied
- Data quality check results
- Error details and line numbers

**Application Logs:**
- Streamlit dashboard access patterns
- Athena query execution times
- Cache hit/miss rates
- User interactions and filter usage

## CloudWatch Dashboards

A custom dashboard displays real-time pipeline health:

- **Pipeline Success Rate** – % of successful daily runs (target: 99%+)
- **Data Volume Trend** – Records flowing through each layer
- **Processing Time Graph** – Duration over time to detect slowdowns
- **Error Trends** – Daily count of errors by component
- **Data Quality Scorecard** – Null %, duplicates %, validation failures %

Access via AWS Console → CloudWatch → Dashboards

## Alerting Strategy

### Alert Triggers

**Critical Alerts** (immediate notification):
1. **Pipeline Failure** – Any DAG task fails
   - Condition: Airflow task status = FAILED
   - Action: Email alert with error log excerpt
   - Resolution: Check CloudWatch Logs, review Lambda/Glue output

2. **Data Quality Failure** – Critical data quality check fails
   - Condition: `DataQualityFailures` > threshold
   - Action: Email alert with quality report
   - Resolution: Investigate source data, review transformation logic

3. **High Error Rate** – Lambda or Glue job error rate > 5%
   - Condition: `ErrorRate` > 0.05
   - Action: Email + Slack notification
   - Resolution: Review error logs, check API health, verify IAM roles

4. **Storage Quota** – Data lake exceeding 80% of quota
   - Condition: `S3BucketSize` > threshold
   - Action: Email alert
   - Resolution: Archive old data, optimize partitioning

### Warning Alerts (daily summary):
- Slow data ingestion (>30 min duration)
- High null value ratio (>10%)
- Duplicate record detection (>1%)
- Query cost exceeding budget (>$10/day)

### Alert Configuration

Alerts are configured in **AWS SNS** with:
- **Email recipients** – Data team distribution list
- **Slack integration** – #data-pipeline channel
- **Escalation policy** – Page on-call engineer after 2 hours unresolved

Environment variables in EC2 IAM role define alert thresholds:
```bash
ALERT_PIPELINE_TIMEOUT=3600  # seconds
ALERT_ERROR_THRESHOLD=0.05   # 5%
ALERT_NULL_THRESHOLD=0.10    # 10%
ALERT_QUOTA_THRESHOLD=0.80   # 80%
```

## Health Checks

### Daily Validation

After each pipeline run, automated checks verify:

1. **Ingestion Completeness** – Expected row count from API received
2. **Schema Validation** – All required columns present and correct types
3. **Referential Integrity** – Location codes match master list
4. **Partition Correctness** – Data partitioned by location as expected
5. **Gold Layer Refresh** – Aggregation updated with latest data

Results stored in DynamoDB `pipeline_health` table with timestamp

### Manual Health Checks

Data engineers can run ad-hoc validation:
```bash
# Verify bronze layer load
aws s3 ls s3://brewery-data-lake-bronze/ --recursive | wc -l

# Query silver layer record count
aws athena start-query-execution \
  --query-string "SELECT COUNT(*) FROM silver.breweries_tb_breweries" \
  --result-configuration OutputLocation=s3://query-results/

# Check gold layer freshness
aws athena start-query-execution \
  --query-string "SELECT MAX(updated_at) FROM gold.tb_ft_breweries_agg" \
  --result-configuration OutputLocation=s3://query-results/
```

## Streamlit Observability Dashboard

The dashboard includes an **Observability** tab showing:

### Active Metrics Panel
- Current pipeline status (running/success/failed)
- Last successful run timestamp
- Records processed today
- Current error count
- Data quality score (%)

### Pipeline History Chart
- Line graph of execution time over past 30 days
- Success/failure rate trend
- Record volume trend

### Error Log Viewer
- Last 100 error events with timestamps
- Error type distribution (pie chart)
- Component breakdown (Lambda vs Glue vs transformation)

### Data Quality Report
- Null value % by column
- Duplicate detection results
- Schema validation summary
- Anomaly detection flags

Access at: `http://ec2-instance:8501` → Observability tab

## Incident Response

### When a Pipeline Fails

1. **Alert received** → Check email/Slack for error summary
2. **Navigate to Airflow UI** → Examine failed task logs
3. **Review CloudWatch** → See full error context with timestamps
4. **Check data** → Query S3/Athena to assess data integrity
5. **Root cause analysis** → Review source code and recent changes
6. **Fix and retry** → Manual trigger via Airflow UI or wait for next scheduled run

### Common Issues & Resolution

| Issue | Cause | Resolution |
|-------|-------|-----------|
| "API timeout" | OpenBreweryDB API slow | Increase timeout env var, retry later |
| "Schema mismatch" | API response format changed | Update Glue schema, notify team |
| "Duplicate records" | Lambda invoked twice | Check Airflow retry logic, investigate |
| "Gold table empty" | Glue job filtered all records | Review silver layer data, check filter logic |

## Monitoring Best Practices

1. **Real-time dashboards** – Check Streamlit Observability tab daily
2. **Log aggregation** – CloudWatch Logs serve as single source of truth
3. **Threshold tuning** – Adjust alert thresholds quarterly based on trends
4. **Cost optimization** – Monitor Athena query costs, optimize partitioning
5. **Capacity planning** – Track S3 growth, plan archival strategy
6. **Documentation** – Keep incident playbooks updated

## Future Enhancements

- [ ] Machine learning anomaly detection on data quality metrics
- [ ] Slack bot for ad-hoc query execution and status checks
- [ ] Automated remediation (e.g., auto-retry, rollback on failure)
- [ ] Advanced data profiling and trend analysis
- [ ] Cost allocation and budget tracking by layer
- [ ] Integration with PagerDuty for on-call escalation
