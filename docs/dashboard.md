# Streamlit Dashboard

This document provides an overview of the interactive Streamlit dashboard for brewery data exploration and analytics.

## Dashboard Overview

The dashboard is a web-based application built with Streamlit, providing three main analytical perspectives on the brewery dataset.

## 📊 Analytics Tab

**Purpose**: Comprehensive data exploration and business intelligence.

**Features**:
- **Interactive Filters**: Filter breweries by state, city, type, and other attributes
- **Data Visualization**: Charts and graphs showing brewery distribution patterns
- **Statistical Analysis**: Key metrics and trends in the brewery industry
- **Export Capabilities**: Download filtered data in multiple formats (CSV, JSON, Parquet)

**Demo Video**: [View Analytics Demo](docs/videos/analytics.mp4)

## 🔍 Observability Tab

**Purpose**: Real-time monitoring of pipeline health and system performance.

**Features**:
- **Pipeline Status**: Live view of Airflow DAG execution status
- **Performance Metrics**: Query performance, data processing times, error rates
- **System Health**: AWS service utilization and resource monitoring
- **Alert Dashboard**: Active alerts and incident tracking

**Demo Video**: [View Observability Demo](docs/videos/observability.mp4)

## 🛡️ Data Quality Tab

**Purpose**: Validation and monitoring of data quality across all pipeline stages.

**Features**:
- **Quality Metrics**: Completeness, accuracy, and consistency scores
- **Data Profiling**: Statistical summaries and data distribution analysis
- **Validation Rules**: Custom business rules and threshold monitoring
- **Quality Reports**: Historical quality trends and issue tracking

**Demo Video**: [View Data Quality Demo](docs/videos/data_quality.mp4)

## Technical Implementation

- **Backend**: Direct connection to AWS Athena for real-time queries
- **Frontend**: Streamlit web application with responsive design
- **Caching**: Intelligent caching for improved performance
- **Security**: AWS IAM authentication and read-only access controls

## User Experience

The dashboard provides an intuitive interface for both technical and business users to:
- Explore brewery data without complex SQL queries
- Monitor pipeline operations in real-time
- Ensure data quality meets business requirements
- Export data for further analysis in external tools

All tabs are designed for self-service analytics while maintaining enterprise-grade security and performance standards.