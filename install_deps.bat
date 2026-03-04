@echo off
REM Install missing dependencies

echo.
echo ============================================================
echo Installing Missing Dependencies...
echo ============================================================
echo.

REM Activate virtual environment first
call venv\Scripts\activate.bat

REM Install plotly and other required packages
pip install --upgrade pip
pip install plotly>=5.0.0
pip install streamlit>=1.28.0
pip install pandas>=2.0.0
pip install boto3>=1.28.0
pip install pyarrow>=12.0.0

echo.
echo ============================================================
echo ✅ All dependencies installed successfully!
echo ============================================================
echo.
echo Next, run:
echo   cd streamlit_app
echo   streamlit run main.py
echo.
pause
