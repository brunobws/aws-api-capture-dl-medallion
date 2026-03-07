# AWS Infrastructure Setup

This document outlines the AWS resources used in the brewery data pipeline and provides guidance for read-only access configuration.

## Core AWS Services

### ☁️ AWS Lambda
**Purpose**: Serverless compute for API data ingestion
- **Runtime**: Python 3.9
- **Triggers**: Scheduled CloudWatch Events
- **Integration**: Direct API calls to Open Brewery DB
- **Scaling**: Automatic scaling based on event frequency

### 🪣 Amazon S3
**Purpose**: Data lake storage with Medallion Architecture
- **Bronze Layer**: Raw, unprocessed data
- **Silver Layer**: Cleaned and transformed data
- **Gold Layer**: Business-ready analytics data
- **Security**: Server-side encryption, versioning enabled

### 🔧 AWS Glue
**Purpose**: ETL processing and metadata management
- **Glue ETL Jobs**: PySpark-based data transformations
- **Glue Catalog**: Centralized metadata repository
- **Crawlers**: Automatic schema discovery
- **Data Quality**: Built-in validation and profiling

### 📊 Amazon Athena
**Purpose**: Serverless SQL queries on S3 data
- **Query Engine**: Presto-based SQL processing
- **Integration**: Direct queries on Glue Catalog tables
- **Performance**: Query result caching and optimization
- **Cost**: Pay-per-query pricing model

### 🗄️ Amazon DynamoDB
**Purpose**: Metadata and configuration storage
- **Tables**: Pipeline configuration, job status tracking
- **Access Patterns**: Fast key-value lookups
- **Scaling**: Automatic throughput scaling

### 📈 Amazon CloudWatch
**Purpose**: Monitoring, logging, and alerting
- **Metrics**: Custom pipeline performance metrics
- **Logs**: Centralized logging from all services
- **Alarms**: Automated alerts for pipeline failures
- **Dashboards**: Real-time monitoring views

### 📧 Amazon SES
**Purpose**: Email notifications and alerts
- **Integration**: Pipeline failure notifications
- **Templates**: Pre-configured alert messages
- **Delivery**: Reliable email delivery service

## Read-Only Access Configuration

### IAM User Setup
For safe exploration and demonstration purposes, a read-only IAM user is provided with the following permissions:

#### S3 Access
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::brewery-data-lake-bronze/*",
        "arn:aws:s3:::brewery-data-lake-silver/*",
        "arn:aws:s3:::brewery-data-lake-gold/*"
      ]
    }
  ]
}
```

#### Athena Query Access
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "athena:StartQueryExecution",
        "athena:GetQueryExecution",
        "athena:GetQueryResults"
      ],
      "Resource": "*"
    }
  ]
}
```

#### Glue Catalog Access
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "glue:GetDatabase",
        "glue:GetDatabases",
        "glue:GetTable",
        "glue:GetTables",
        "glue:GetPartition",
        "glue:GetPartitions"
      ],
      "Resource": "*"
    }
  ]
}
```

### Security Best Practices
- **Least Privilege**: Only necessary read permissions granted
- **No Write Access**: Prevents accidental data modification
- **Audit Logging**: All access attempts are logged
- **Temporary Credentials**: Short-lived credentials recommended

This setup ensures stakeholders can explore and analyze the data lake safely while maintaining data integrity and security.