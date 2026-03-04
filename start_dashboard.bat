@echo off
REM ====================================================================
REM Data Platform Dashboard Launcher
REM ====================================================================
REM
REM This script starts the Streamlit dashboard for the Medallion Data Lake
REM monitoring platform.
REM
REM Requirements:
REM - Python 3.8+
REM - Dependencies installed (pip install -r requirements.txt)
REM - AWS credentials configured (AWS_REGION, etc.)
REM
REM Usage:
REM   1. Open PowerShell or CMD
REM   2. Navigate to project root directory
REM   3. Run: start_dashboard.bat
REM   4. Dashboard opens automatically at http://localhost:8501
REM
REM ====================================================================

setlocal enabledelayedexpansion

cls

echo.
echo ====================================================================
echo  📊 Data Platform Monitoring & Analytics Dashboard
echo ====================================================================
echo.

REM Check if in project root
if not exist "streamlit_app" (
    echo ❌ ERROR: streamlit_app folder not found
    echo.
    echo Please run this script from the project root directory.
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
if not exist "venv" (
    echo ⚠️  Virtual environment not found.
    echo.
    echo To set up the environment, run:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Navigate to streamlit app directory
cd streamlit_app

REM Start the dashboard
echo ✅ Starting dashboard service...
echo.
echo 📌 Dashboard URL: http://localhost:8501
echo 📌 Press Ctrl+C to stop
echo.
echo ====================================================================
echo.

streamlit run main.py

pause
