# Architecture Overview

This document provides a detailed explanation of the Medallion Architecture implemented in this AWS Data Lake project.

## Architecture Layers

### 🏗️ Ingestion Layer
The ingestion layer is responsible for collecting data from external sources and bringing it into the data lake.

- **AWS Lambda Functions**: Serverless functions that trigger API calls to the Open Brewery DB API
- **Event-driven ingestion**: Automated data collection on scheduled intervals
- **Raw data landing**: Initial data storage in the Bronze layer without transformations

### 🗄️ Storage Layer
Data is organized in a multi-tiered storage approach following the Medallion Architecture pattern.

- **Bronze Layer (Raw)**: Raw, unprocessed data stored in Amazon S3
- **Silver Layer (Cleaned)**: Transformed and validated data with basic cleansing
- **Gold Layer (Curated)**: Business-ready data optimized for analytics and reporting

### ⚙️ Processing Layer
Data transformations and processing are handled through AWS Glue with PySpark.

- **AWS Glue ETL Jobs**: Serverless ETL processing using PySpark
- **Data Quality Checks**: Automated validation and cleansing operations
- **Metadata Management**: AWS Glue Catalog for schema discovery and management

### 📊 Data Consumption Layer
Multiple interfaces for data access and analytics.

- **AWS Athena**: Serverless SQL queries directly on S3 data
- **Streamlit Dashboard**: Interactive web application for data exploration
- **API Endpoints**: Programmatic access to processed data

### 🔍 Observability Layer
Comprehensive monitoring and logging across all components.

- **Amazon CloudWatch**: Metrics, logs, and alerts for AWS services
- **Custom Logging**: Application-level logging with structured data
- **Dashboard Monitoring**: Real-time pipeline health and performance metrics

### 🔐 Security & Governance
Enterprise-grade security and access controls.

- **IAM Roles and Policies**: Least-privilege access to AWS resources
- **Read-only Access**: Safe exploration environment for stakeholders
- **Data Encryption**: At-rest and in-transit encryption for sensitive data
- **Audit Logging**: Comprehensive audit trails for compliance

## Data Flow

1. **Ingestion**: Lambda functions collect data from APIs and store in Bronze S3
2. **Processing**: Glue jobs transform Bronze → Silver → Gold layers
3. **Cataloging**: Glue Catalog maintains metadata and schemas
4. **Consumption**: Athena and dashboard provide access to Gold layer data
5. **Monitoring**: CloudWatch tracks performance and alerts on issues

This architecture ensures scalability, reliability, and maintainability while following AWS best practices for data lake implementations.