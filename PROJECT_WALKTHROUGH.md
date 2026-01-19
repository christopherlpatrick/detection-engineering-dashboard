# Detection Engineering Simulation Dashboard - Project Walkthrough

## Overview
This is a comprehensive SOC portfolio project that demonstrates detection engineering capabilities through simulated identity and cloud attack scenarios. The dashboard visualizes detections, investigation workflows, and response metrics in a professional, interview-ready format.

## How to Demo in an Interview

### 1. **Start with Executive Overview**
- Navigate to the Executive Security Overview page
- Highlight the KPIs: Total Alerts, High Severity Alerts, Impacted Users, MTTD, MTTR
- Show the trend charts demonstrating alert patterns over time
- Explain how filters allow drill-down by date range, user, scenario type, and severity
- **Key Talking Point**: "This provides SOC leadership with real-time visibility into security posture and response effectiveness"

### 2. **Demonstrate Attack Scenarios**
- Navigate to the Attack Timeline page
- Show the 4 simulated attack scenarios:
  - **MFA Fatigue**: Explain how 8-15 failed MFA prompts followed by success indicates an attack
  - **Impossible Travel**: Show how authentication from New York and Tokyo within 30 minutes triggers detection
  - **OAuth Consent Abuse**: Demonstrate high-risk scope detection
  - **Privilege Escalation**: Show off-hours role assignment detection
- Click on events to show the MITRE ATT&CK mapping
- **Key Talking Point**: "Each scenario represents real-world attack patterns we need to detect in production"

### 3. **Showcase Detection Engineering**
- Navigate to the Detection Library page
- Click on a detection (e.g., "MFA Fatigue Attack")
- Explain the detection logic in plain English
- Show the required signals, expected false positives, and recommended response
- Highlight the MITRE ATT&CK mapping (Tactic, Technique, Technique ID)
- Show example events that triggered the detection
- **Key Talking Point**: "These are production-ready detection rules with clear logic, false positive expectations, and response playbooks"

### 4. **Investigation Workflow**
- Navigate to the Investigation Drill-Down page
- Enter a user email (e.g., "alice.johnson@company.com")
- Show the comprehensive investigation panel:
  - Sign-in history with geolocation changes
  - MFA prompt history
  - OAuth app consents with scopes
  - Role assignment changes
  - Correlated alerts and incidents
- **Key Talking Point**: "This demonstrates how an analyst would pivot from an alert to a full user investigation, following the chain of evidence"

### 5. **Response Actions & Metrics**
- Navigate to the Response Actions page
- Select an incident
- Execute simulated response actions:
  - Disable User
  - Revoke Sessions
  - Require Password Reset
  - Isolate Endpoint
  - Block OAuth App
- Show how incident status progresses: Open → Investigating → Contained → Resolved
- Highlight the MTTR calculation
- **Key Talking Point**: "This simulates the incident response workflow and tracks key metrics like time to contain and time to resolve"

### 6. **Technical Architecture (if asked)**
- **Backend**: FastAPI with SQLAlchemy ORM, SQLite database
- **Frontend**: React with Vite, Recharts for visualizations, Tailwind CSS
- **Data Model**: Comprehensive security event schema with all required fields
- **Detection Logic**: Rule-based detection engine with MITRE ATT&CK mapping
- **API Design**: RESTful endpoints with filtering, pagination, and drill-down capabilities

### 7. **Key Strengths to Emphasize**
- **Detection Engineering Focus**: Not just monitoring, but building and tuning detection rules
- **MITRE ATT&CK Mapping**: Every detection is mapped to the framework
- **Realistic Scenarios**: Based on actual attack patterns (MFA fatigue, impossible travel, etc.)
- **Investigation Workflow**: Shows how to pivot from alert to full investigation
- **Metrics-Driven**: Tracks MTTD, MTTR, and other SOC KPIs
- **Professional UI**: Clean, modern interface suitable for SOC operations

## Technical Implementation Highlights

- **Data Generation**: Realistic attack scenario simulation with proper event sequencing
- **Detection Rules**: 8 detection rules covering identity and cloud security
- **API Design**: Comprehensive endpoints for all dashboard views
- **Frontend**: 5 interactive pages with filtering, drill-down, and visualization
- **Response Simulation**: Realistic incident response workflow with status tracking

## What Makes This Portfolio-Ready

1. **Comprehensive Coverage**: Covers the full detection engineering lifecycle
2. **Professional Presentation**: Clean UI suitable for SOC operations
3. **Real-World Scenarios**: Based on actual attack patterns
4. **Metrics & KPIs**: Demonstrates understanding of SOC metrics
5. **Investigation Workflow**: Shows analytical thinking and investigation skills
6. **MITRE ATT&CK**: Demonstrates knowledge of the framework
7. **Code Quality**: Well-structured, maintainable codebase
