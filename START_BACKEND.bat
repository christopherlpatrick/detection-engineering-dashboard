@echo off
echo ========================================
echo Detection Engineering Dashboard Backend
echo ========================================
echo.

cd /d "%~dp0backend"
if errorlevel 1 (
    echo Error: Could not navigate to backend directory
    pause
    exit /b 1
)

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Installing/updating dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

if not exist detection_engineering.db (
    echo Generating sample data...
    python generate_data.py
    if errorlevel 1 (
        echo Warning: Failed to generate data, continuing anyway...
    )
)

echo.
echo ========================================
echo Starting backend server...
echo Backend will be available at: http://localhost:8000
echo API docs will be at: http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo ========================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
