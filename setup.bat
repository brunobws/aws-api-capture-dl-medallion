@echo off
REM Breweries Dashboard - Setup Script for Windows
REM This script sets up the project environment automatically

echo.
echo ========================================
echo Breweries Dashboard - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Verifying AWS configuration...
aws sts get-caller-identity >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: AWS credentials not configured
    echo.
    echo Please configure AWS:
    echo   1. Run: aws configure
    echo   2. Enter your AWS Access Key ID
    echo   3. Enter your AWS Secret Access Key
    echo   4. Set default region to: sa-east-1
    echo.
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the dashboard:
echo   1. Activate virtual environment:
echo      venv\Scripts\activate
echo   2. Run Streamlit:
echo      streamlit run streamlit_app/main.py
echo.
echo The dashboard will open at: http://localhost:8501
echo.
pause
