# Detection Engineering Simulation Dashboard

A comprehensive SOC portfolio project that simulates identity and cloud attack scenarios, displays detections, and visualizes investigation and response metrics.

## Features

- **4 Attack Scenarios**: MFA Fatigue, Impossible Travel, OAuth Consent Abuse, Privilege Escalation
- **8 Detection Rules**: Mapped to MITRE ATT&CK framework with complete documentation
- **5 Interactive Dashboard Pages**: Executive Overview, Attack Timeline, Detection Library, Investigation Drill-Down, Response Actions
- **Real-time Metrics**: MTTD, MTTR, alert trends, and security KPIs

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, SQLite
- **Frontend**: React, Vite, Recharts, Tailwind CSS
- **Data**: Simulated security events with realistic attack patterns

## Quick Start

### Backend Setup

```bash
cd detection-engineering-dashboard/backend
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python generate_data.py
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup

```bash
cd detection-engineering-dashboard/frontend
npm install
npm run dev
```

Access the dashboard at http://localhost:5173

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

## Key Features

### Detection Engineering
- 8 detection rules with MITRE ATT&CK mappings
- Detection logic, required signals, false positive expectations
- Recommended response actions for each detection

### Attack Scenarios
- **MFA Fatigue**: 8-15 failed MFA prompts followed by success
- **Impossible Travel**: Authentication from distant locations within impossible timeframes
- **OAuth Consent Abuse**: High-risk OAuth app consents with dangerous scopes
- **Privilege Escalation**: Off-hours privileged role assignments followed by suspicious activity

### Dashboard Pages
1. **Executive Overview**: KPIs, alert trends, MITRE tactic analysis
2. **Attack Timeline**: Visual timeline of attack scenarios with event sequences
3. **Detection Library**: Engineering view with detection rule details
4. **Investigation Drill-Down**: User investigation with sign-in history, geolocation changes, OAuth consents
5. **Response Actions**: Simulated incident response workflow

## API Endpoints

- `/api/v1/dashboard/kpis` - Dashboard KPIs
- `/api/v1/dashboard/alert-trends` - Alert trends over time
- `/api/v1/detections` - All detection rules
- `/api/v1/events` - Security events
- `/api/v1/incidents` - Incidents
- `/api/v1/users/{user}/investigation` - User investigation data
- `/api/v1/incidents/{incident_id}/response/{action_type}` - Execute response action

Full API documentation available at http://localhost:8000/docs

## Data Generated

- 249+ security events (200 normal + 50+ attack scenario events)
- 9 alerts (one per attack scenario)
- 9 incidents
- 8 detection rules

## Technologies Used

**Backend:**
- Python 3.9+
- FastAPI 0.104.1
- SQLAlchemy 2.0.45
- Uvicorn

**Frontend:**
- React 18
- Vite 5
- Recharts 2.10.3
- Tailwind CSS 3.3.6
- Axios 1.6.2

## License

This project is part of a portfolio demonstration.

## Author

Christopher Patrick
