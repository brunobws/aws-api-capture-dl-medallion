# Airflow Orchestration

This document details the Apache Airflow implementation for orchestrating the brewery data pipeline.

## DAG Overview

The `brewery_pipeline.py` DAG manages the end-to-end data processing workflow with the following key characteristics:

- **Schedule**: Daily execution at 2:00 AM UTC
- **Retries**: 3 retry attempts with exponential backoff
- **Dependencies**: Sequential task execution with proper upstream/downstream relationships
- **Monitoring**: Comprehensive logging and alerting

## Pipeline Tasks

### 1. 🔄 API Ingestion
- **Task**: `ingest_brewery_data`
- **Purpose**: Collects brewery data from Open Brewery DB API
- **Technology**: AWS Lambda function invocation
- **Output**: Raw JSON data stored in Bronze S3 bucket

### 2. 📥 Bronze Layer Ingestion
- **Task**: `bronze_ingestion`
- **Purpose**: Validates and stores raw data in Bronze layer
- **Technology**: AWS Glue job for initial data validation
- **Checks**: Schema validation, duplicate detection, basic data quality

### 3. 🧹 Bronze to Silver Transformation
- **Task**: `bronze_to_silver`
- **Purpose**: Cleans and standardizes data
- **Technology**: AWS Glue PySpark job
- **Operations**: Data type conversions, null handling, standardization

### 4. ✨ Silver to Gold Transformation
- **Task**: `silver_to_gold`
- **Purpose**: Creates business-ready datasets
- **Technology**: AWS Glue PySpark job
- **Operations**: Aggregation, enrichment, final data quality checks

### 5. ✅ Data Quality Validation
- **Task**: `data_quality_checks`
- **Purpose**: Validates data integrity across all layers
- **Technology**: Custom PySpark validation functions
- **Metrics**: Completeness, accuracy, consistency checks

### 6. 📊 Logging and Monitoring
- **Task**: `log_pipeline_metrics`
- **Purpose**: Records pipeline execution metrics
- **Technology**: CloudWatch custom metrics and logs
- **Outputs**: Execution time, success/failure rates, data volumes

## DAG Dependencies

```
ingest_brewery_data
        ↓
bronze_ingestion
        ↓
bronze_to_silver
        ↓
silver_to_gold
        ↓
data_quality_checks
        ↓
log_pipeline_metrics
```

## Error Handling

- **Automatic Retries**: Failed tasks retry up to 3 times
- **Alerting**: Email notifications on pipeline failures
- **Logging**: Detailed error logs stored in CloudWatch
- **Recovery**: Manual trigger capability for failed pipelines

## Monitoring Dashboard

The Airflow web UI provides real-time visibility into:
- Task execution status
- Pipeline duration and performance
- Error logs and troubleshooting information
- Historical run data and trends

This orchestration ensures reliable, scheduled data processing with comprehensive monitoring and error recovery capabilities.