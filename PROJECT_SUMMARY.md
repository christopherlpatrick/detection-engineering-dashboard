# Detection Engineering Simulation Dashboard - Project Summary

## What Was Built

A complete, portfolio-ready Detection Engineering Simulation Dashboard that demonstrates SOC operations, detection engineering, and incident response capabilities.

## Key Features

### ✅ Data Model
- Comprehensive security event schema with all 20+ required fields
- Support for identity and cloud security events
- Proper relationships between events, alerts, incidents, and detections

### ✅ Attack Scenarios (4)
1. **MFA Fatigue**: 8-15 failed MFA prompts followed by successful authentication
2. **Impossible Travel**: Authentication from distant locations within impossible timeframes
3. **OAuth Consent Abuse**: High-risk OAuth app consents with dangerous scopes
4. **Privilege Escalation**: Off-hours privileged role assignments followed by suspicious activity

### ✅ Detection Rules (8)
1. MFA Fatigue Attack (DET-001) - T1110.001
2. Impossible Travel (DET-002) - T1078
3. Legacy Authentication Usage (DET-003) - T1562.001
4. Risky Sign-In with High Risk (DET-004) - T1078
5. OAuth App Consent with High-Risk Scopes (DET-005) - T1078.004
6. Privileged Role Assignment Outside Business Hours (DET-006) - T1078.004
7. Azure Resource Creation from Unusual Location (DET-007) - T1496
8. Suspicious Policy Change (DET-008) - T1562.001

Each detection includes:
- Detection logic (plain English)
- Required signals
- Expected false positives
- Recommended response
- MITRE ATT&CK mapping

### ✅ Dashboard Pages (5)

#### 1. Executive Security Overview
- KPIs: Total alerts, high severity alerts, impacted users, MTTD, MTTR
- Trend charts: Alerts over time, sign-in stats, MFA stats
- Top MITRE tactics visualization
- Comprehensive filtering (date, user, scenario, severity)

#### 2. Attack Timeline
- Visual timeline of attack scenarios
- Event sequences (pre-attack → attack → detection → response)
- Click events to view details and MITRE mappings
- Filter by scenario type and user

#### 3. Detection Library
- Table of all detection rules
- Click to view full details:
  - Detection logic
  - Required signals
  - False positive expectations
  - Response playbooks
  - Example triggering events
- Search and filter capabilities

#### 4. Investigation Drill-Down
- Per-user investigation panel
- Sign-in history with geolocation changes
- MFA prompt history
- OAuth app consents with scopes
- Role assignment changes
- Correlated alerts and incidents
- Pivot from user to IPs, devices, apps

#### 5. Response Actions
- Simulated incident response workflow
- 5 response actions:
  - Disable User
  - Revoke Sessions
  - Require Password Reset
  - Isolate Endpoint
  - Block OAuth App
- Incident status tracking: Open → Investigating → Contained → Resolved
- MTTR calculation
- Action history

## Technical Stack

### Backend
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: SQLite (easily switchable to PostgreSQL)
- **API**: RESTful with comprehensive filtering and pagination

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Charts**: Recharts
- **Styling**: Tailwind CSS
- **Icons**: Lucide React

## Project Structure

```
detection-engineering-dashboard/
├── backend/
│   ├── app/
│   │   ├── models.py              # Database models
│   │   ├── schemas.py             # Pydantic schemas
│   │   ├── main.py                # FastAPI application
│   │   └── routers/               # API endpoints
│   │       ├── dashboard.py       # KPI and trend endpoints
│   │       ├── detections.py      # Detection rules endpoints
│   │       ├── events.py          # Security events endpoints
│   │       ├── incidents.py      # Incidents and investigation
│   │       └── response_actions.py # Response action endpoints
│   ├── generate_data.py          # Data generation script
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/                 # 5 dashboard pages
│   │   │   ├── ExecutiveOverview.jsx
│   │   │   ├── AttackTimeline.jsx
│   │   │   ├── DetectionLibrary.jsx
│   │   │   ├── InvestigationDrillDown.jsx
│   │   │   └── ResponseActions.jsx
│   │   ├── components/
│   │   │   └── Layout.jsx         # Navigation layout
│   │   ├── services/
│   │   │   └── api.js             # API client
│   │   └── App.jsx
│   └── package.json
├── README.md
├── QUICKSTART.md
├── PROJECT_WALKTHROUGH.md
├── RESUME_BULLETS.md
└── PROJECT_SUMMARY.md
```

## Data Generated

- **Security Events**: ~250+ events (200 normal + 50+ attack scenario events)
- **Alerts**: 9+ alerts (one per attack scenario)
- **Incidents**: 9+ incidents
- **Detections**: 8 detection rules
- **Response Actions**: Generated when executed in UI

## Key Highlights

1. **Realistic Attack Scenarios**: Based on actual attack patterns seen in production
2. **MITRE ATT&CK Mapping**: Every detection mapped to the framework
3. **Investigation Workflow**: Shows how to pivot from alert to full investigation
4. **Metrics Tracking**: MTTD, MTTR, and other SOC KPIs
5. **Professional UI**: Clean, modern interface suitable for SOC operations
6. **Comprehensive Filtering**: Drill down by date, user, scenario, severity
7. **Response Simulation**: Realistic incident response workflow

## Next Steps

1. **Run the Project**: Follow QUICKSTART.md
2. **Review Walkthrough**: See PROJECT_WALKTHROUGH.md for demo guidance
3. **Customize**: Add your own attack scenarios or detection rules
4. **Deploy**: Can be deployed to Heroku, Railway, Vercel, etc.
5. **Enhance**: Add authentication, more visualizations, or additional scenarios

## Portfolio Readiness

This project is ready for:
- ✅ GitHub portfolio
- ✅ Interview demonstrations
- ✅ Resume bullet points (see RESUME_BULLETS.md)
- ✅ Technical discussions about detection engineering
- ✅ SOC operations discussions

## Skills Demonstrated

- Detection Engineering
- MITRE ATT&CK Framework
- SOC Operations
- Incident Response
- Full-Stack Development (Python, React)
- API Design
- Data Modeling
- Security Metrics (MTTD, MTTR)
- Investigation Workflows
