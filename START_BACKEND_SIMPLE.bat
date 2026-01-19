@echo off
cd /d "%~dp0backend"
call venv\Scripts\activate.bat
echo Starting backend server...
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
