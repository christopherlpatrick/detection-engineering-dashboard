# How to Run the Detection Engineering Dashboard

## Quick Start (Windows)

### Option 1: Use Batch Files (Easiest)

1. **Start Backend** (Terminal 1):
   - Double-click `START_BACKEND.bat`
   - Wait for it to install dependencies and start (takes 1-2 minutes first time)
   - You should see: "Uvicorn running on http://127.0.0.1:8000"

2. **Start Frontend** (Terminal 2):
   - Double-click `START_FRONTEND.bat`
   - Wait for it to install dependencies and start (takes 1-2 minutes first time)
   - You should see: "Local: http://localhost:5173"

3. **Open Browser**:
   - Go to http://localhost:5173
   - The dashboard should load!

### Option 2: Manual Commands

#### Terminal 1 - Backend:
```powershell
cd detection-engineering-dashboard\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python generate_data.py
uvicorn app.main:app --reload
```

#### Terminal 2 - Frontend:
```powershell
cd detection-engineering-dashboard\frontend
npm install
npm run dev
```

## What You'll See

- **Backend**: Running on http://localhost:8000
- **Frontend**: Running on http://localhost:5173
- **API Docs**: http://localhost:8000/docs

## Troubleshooting

### "Connection Refused" Error
- Make sure the backend is running first (Terminal 1)
- Check that you see "Uvicorn running on http://127.0.0.1:8000" in the backend terminal

### "Module not found" Error
- Make sure you activated the virtual environment: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### "Port already in use" Error
- Close any other applications using port 8000 or 5173
- Or change the port in the configuration files

### Frontend can't connect to backend
- Make sure backend is running on port 8000
- Check that CORS is enabled (it should be by default)

## First Time Setup

The first time you run it:
1. Backend will create a virtual environment (venv folder)
2. Backend will install Python packages (takes 1-2 minutes)
3. Backend will generate sample data (creates database with attack scenarios)
4. Frontend will install Node packages (takes 1-2 minutes)

After that, it starts much faster!

## Stopping the Servers

- Press `Ctrl+C` in each terminal window to stop the servers
- Or just close the terminal windows
