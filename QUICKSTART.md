# Quick Start Guide

## Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

## Backend Setup

1. Navigate to backend directory:
```bash
cd detection-engineering-dashboard/backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Generate sample data:
```bash
python generate_data.py
```

6. Start the server:
```bash
uvicorn app.main:app --reload
```

The backend will run on http://localhost:8000

## Frontend Setup

1. Open a new terminal and navigate to frontend directory:
```bash
cd detection-engineering-dashboard/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

The frontend will run on http://localhost:5173

## Access the Dashboard

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Project Structure

```
detection-engineering-dashboard/
├── backend/
│   ├── app/
│   │   ├── models.py          # Database models
│   │   ├── schemas.py          # Pydantic schemas
│   │   ├── main.py             # FastAPI app
│   │   └── routers/            # API endpoints
│   ├── generate_data.py        # Data generation script
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/              # Dashboard pages
│   │   ├── components/         # Reusable components
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## First Steps

1. **Generate Data**: Run `python generate_data.py` to create sample attack scenarios
2. **Explore Dashboard**: Navigate through the 5 pages:
   - Executive Overview
   - Attack Timeline
   - Detection Library
   - Investigation Drill-Down
   - Response Actions
3. **Review Detections**: Check the Detection Library to see all 8 detection rules
4. **Investigate Users**: Use the Investigation page to drill down into user activity
5. **Test Response Actions**: Select an incident and execute simulated response actions

## Troubleshooting

- **Database errors**: Delete `detection_engineering.db` and run `generate_data.py` again
- **Port conflicts**: Change ports in `vite.config.js` (frontend) or `main.py` (backend)
- **CORS errors**: Ensure backend is running and CORS is configured in `main.py`

## Next Steps

- Review the PROJECT_WALKTHROUGH.md for demo guidance
- Check RESUME_BULLETS.md for resume content
- Customize detection rules in `generate_data.py`
- Add your own attack scenarios
