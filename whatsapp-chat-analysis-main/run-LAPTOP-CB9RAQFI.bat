@echo off
REM Startup script for WhatsApp Chat Analyzer
REM This script starts the Streamlit frontend

echo.
echo ========================================
echo   WhatsApp Chat Analyzer
echo   Version 2.0.0
echo ========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call c:\Users\HP\OneDrive\Desktop\whatsapp-chat-analysis-main\.venv-1\Scripts\activate.bat

REM Check if dependencies are installed
echo Checking dependencies...
c:\Users\HP\OneDrive\Desktop\whatsapp-chat-analysis-main\.venv-1\Scripts\python.exe -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    c:\Users\HP\OneDrive\Desktop\whatsapp-chat-analysis-main\.venv-1\Scripts\python.exe -m pip install -r requirements.txt -q
)

REM Download NLTK data if needed
echo Setting up NLP resources...
c:\Users\HP\OneDrive\Desktop\whatsapp-chat-analysis-main\.venv-1\Scripts\python.exe -c "import nltk; import os; if not os.path.exists(os.path.join(nltk.data.find('tokenizers/punkt'), 'english.pickle')): nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True)" 2>nul

echo.
echo ========================================
echo   Starting Application
echo ========================================
echo.

REM Start Streamlit Frontend
echo Starting Streamlit Frontend (Port 8501)...
timeout /t 2 /nobreak

REM Run Streamlit
c:\Users\HP\OneDrive\Desktop\whatsapp-chat-analysis-main\.venv-1\Scripts\python.exe -m streamlit run --server.headless false app_enhanced.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo An error occurred!
    pause
)

