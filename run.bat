@echo off
REM Anomaly Report Analyzer - Master Launch Script

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo   ANOMALY REPORT ANALYZER - SYSTEM LAUNCHER
echo ================================================================================
echo.

REM Check if Node.js is installed
echo Checking prerequisites...
where node >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo ^✓ Node.js found
echo ^✓ Python found
echo.

REM Create virtual environment if not exists
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ^✓ Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ^✓ Virtual environment activated

REM Install/update Python dependencies
echo.
echo Installing Python dependencies...
pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo ^✓ Python dependencies installed

REM Install frontend dependencies
echo.
echo Installing frontend dependencies...
cd frontend
call npm install --silent
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
)
echo ^✓ Frontend dependencies installed
cd ..

REM Display startup information
echo.
echo ================================================================================
echo   STARTING SERVICES
echo ================================================================================
echo.
echo FRONTEND:  http://localhost:3001
echo BACKEND:   http://localhost:5000
echo.
echo Press Ctrl+C to stop all services
echo.
echo ================================================================================
echo.

REM Start backend in a new window
echo Starting Backend Server...
start "Anomaly Analyzer - Backend" cmd /k "venv\Scripts\activate.bat && python app.py"

REM Give backend time to start
timeout /t 3 /nobreak

REM Start frontend
echo Starting Frontend Server...
cd frontend
call npm start

pause
