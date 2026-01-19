@echo off
echo Starting Detection Engineering Dashboard Frontend...
cd frontend
if not exist node_modules (
    echo Installing dependencies...
    call npm install
)
echo Starting frontend server on http://localhost:5173
echo.
npm run dev
pause
