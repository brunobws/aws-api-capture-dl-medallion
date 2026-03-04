"""
Quick Start Guide for Data Platform Dashboard v2.0

This file provides step-by-step instructions to get the dashboard running.
"""

# ==================== QUICKSTART ====================

## 1. ACTIVATE VIRTUAL ENVIRONMENT

### Windows:
venv\Scripts\activate

### macOS/Linux:
source venv/bin/activate


## 2. INSTALL DEPENDENCIES (if not already installed)

pip install -r requirements.txt


## 3. CONFIGURE AWS CREDENTIALS

### Option A: AWS CLI (Recommended)
aws configure
# Enter:
#   AWS Access Key ID: [your-key]
#   AWS Secret Access Key: [your-secret]
#   Default region: sa-east-1
#   Default output format: json


## 4. START DASHBOARD

cd streamlit_app
streamlit run main.py


## 5. OPEN IN BROWSER

# Streamlit will automatically open:
# http://localhost:8501

# Or manually navigate to this URL


# ==================== FIRST TIME SETUP ====================

## Verify AWS Connection

1. Go to any tab
2. Check sidebar for "⚙️ Controls" section
3. If green checkmark shows, AWS is connected ✅
4. If red X shows, check your AWS credentials


## Load Your First Data

### Tab 1: Gold Analytics
1. Click on "📊 Gold – Analytics" tab
2. Multiselect some countries/states
3. View breweries data and charts

### Tab 2: Logs Observability  
1. Click on "📈 Logs – Observability" tab
2. Select some layers (bronze, silver, gold)
3. See pipeline execution health

### Tab 3: Data Quality
1. Click on "🧪 Data Quality" tab
2. Check BDQ-enabled checkbox
3. View data quality test results


# ==================== ENVIRONMENT VARIABLES ====================

## Optional: Set for custom configuration

export AWS_REGION=sa-east-1
export ATHENA_DATABASE=gold
export ATHENA_LOGS_DATABASE=logs
export ATHENA_S3_OUTPUT=s3://bws-dl-logs-sae1-prd/athena/query_results/
export LOG_LEVEL=INFO


# ==================== COMMON ISSUES ====================

## Issue: "Connection Failed"

Solution:
1. Run: aws sts get-caller-identity
2. Should show your AWS account info
3. If fails, run: aws configure
4. Re-enter your credentials


## Issue: "No data returned"

Solution:
1. Check that tables exist:
   - gold.tb_ft_breweries_agg
   - logs.execution_logs
2. Verify you have SELECT permission
3. Check logs for query errors


## Issue: Slow loading

Solution:
1. Try smaller date ranges
2. Reduce number of selected filters
3. Wait for cache to warm up (5 minutes)
4. Check AWS Athena console for slow queries


# ==================== USEFUL COMMANDS ====================

# View dashboard logs
streamlit logs

# Run with verbose logging
LOG_LEVEL=DEBUG streamlit run main.py

# Test Athena connection
python -c "
from utils.athena_service import AthenaService
service = AthenaService()
print('Healthy:', service.health_check())
"

# Clear Streamlit cache
streamlit cache clear


# ==================== PRODUCTION DEPLOYMENT ====================

1. Set up Docker container (see docker/ folder)
2. Configure environment variables in CloudFormation/ECS
3. Use AWS secrets manager for credentials
4. Deploy behind ALB with HTTPS
5. Enable authentication (OAuth2/SSO)
6. Monitor in CloudWatch


# ==================== NEED HELP? ====================

Check README_V2.md for detailed documentation:
- Complete architecture description
- Data table schema
- Configuration options
- Troubleshooting guide
- Security best practices
