"""
Configuration module for Breweries Dashboard.

This module contains all configuration constants and settings for the application.

Author: Data Team
Version: 1.0.0
"""

import os
from pathlib import Path

# Application metadata
APP_NAME = "Breweries Dashboard"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Interactive dashboard for exploring and analyzing brewery aggregation data from AWS Athena"

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
STREAMLIT_DIR = PROJECT_ROOT / "streamlit_app"
ASSETS_DIR = STREAMLIT_DIR / "assets"

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "sa-east-1")
ATHENA_DATABASE = "gold"
ATHENA_TABLE = "tb_ft_breweries_agg"
ATHENA_S3_OUTPUT = "s3://bws-dl-logs-sae1-prd/athena/query_results/"

# Streamlit UI Configuration
STREAMLIT_LAYOUT = "wide"
STREAMLIT_THEME = "light"
STREAMLIT_INITIAL_SIDEBAR_STATE = "expanded"

# Data Configuration
DEFAULT_ROWS_TO_DISPLAY = 1000
MAX_ROWS_TO_DISPLAY = 10000
DATA_REFRESH_INTERVAL = 300  # 5 minutes in seconds

# Column Mappings (customize based on your actual table structure)
COLUMN_DISPLAY_NAMES = {
    "brewery_id": "Brewery ID",
    "brewery_name": "Brewery Name",
    "brewery_type": "Brewery Type",
    "city": "City",
    "state": "State",
    "country": "Country",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "postal_code": "Postal Code",
    "phone": "Phone",
    "website_url": "Website",
    "aggregate_count": "Aggregate Count",
    "last_updated": "Last Updated",
}

# Chart Configuration
CHART_HEIGHT = 400
CHART_WIDTH = None  # Auto width

# Cache Configuration
ENABLE_CACHE = True
CACHE_TTL = 300  # 5 minutes

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Feature Flags
ENABLE_EXPORT = True
ENABLE_STATISTICS = True
ENABLE_MAP_VIEW = True
ENABLE_FILTERS = True

# Display Settings
SHOW_ROW_NUMBERS = True
USE_CONTAINER_WIDTH = True

# Default query for initial load
DEFAULT_QUERY = f"""
SELECT *
FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
LIMIT {DEFAULT_ROWS_TO_DISPLAY}
"""

# Sample queries for quick access
SAMPLE_QUERIES = {
    "Top 10 Breweries by Count": f"""
SELECT
    brewery_name,
    COUNT(*) as total_count
FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
GROUP BY brewery_name
ORDER BY total_count DESC
LIMIT 10
    """,
    "Breweries by State": f"""
SELECT
    state,
    COUNT(DISTINCT brewery_id) as brewery_count,
    COUNT(*) as total_records
FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
GROUP BY state
ORDER BY total_records DESC
    """,
    "Recent Updates": f"""
SELECT *
FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
WHERE last_updated IS NOT NULL
ORDER BY last_updated DESC
LIMIT 100
    """,
}
