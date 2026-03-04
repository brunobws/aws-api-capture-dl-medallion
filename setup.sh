#!/bin/bash
# Breweries Dashboard - Setup Script for macOS/Linux
# This script sets up the project environment automatically

echo ""
echo "========================================"
echo "Breweries Dashboard - Setup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org"
    exit 1
fi

echo "Python version:"
python3 --version

# Create virtual environment
echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "[2/4] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "[3/4] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Verify AWS configuration
echo "[4/4] Verifying AWS configuration..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo ""
    echo "WARNING: AWS credentials not configured"
    echo ""
    echo "Please configure AWS:"
    echo "  1. Run: aws configure"
    echo "  2. Enter your AWS Access Key ID"
    echo "  3. Enter your AWS Secret Access Key"
    echo "  4. Set default region to: sa-east-1"
    echo ""
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the dashboard:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo "  2. Run Streamlit:"
echo "     streamlit run streamlit_app/main.py"
echo ""
echo "The dashboard will open at: http://localhost:8501"
echo ""
