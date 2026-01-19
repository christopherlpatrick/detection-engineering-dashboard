"""
Generate sample data for Detection Engineering Simulation Dashboard
Creates realistic attack scenarios: MFA Fatigue, Impossible Travel, OAuth Consent Abuse, Privilege Escalation
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import (
    Base, engine, SessionLocal, SecurityEvent, Detection, Alert, Incident,
    RiskLevel, SeverityLevel, SignInResult, MFAResult, AzureActivityType, IncidentStatus
)
from datetime import datetime, timedelta
import random
import json

# Initialize database
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Sample data
USERS = ["alice.johnson@company.com", "bob.smith@company.com", "charlie.brown@company.com", 
         "diana.prince@company.com", "eve.wilson@company.com", "frank.miller@company.com",
         "grace.lee@company.com", "henry.davis@company.com"]

IP_ADDRESSES = ["192.168.1.100", "10.0.0.45", "172.16.0.23", "203.0.113.42", 
                "198.51.100.15", "203.0.113.89", "198.51.100.203"]

GEO_LOCATIONS = [
    {"country": "United States", "city": "New York", "ip": "203.0.113.42"},
    {"country": "United States", "city": "San Francisco", "ip": "198.51.100.15"},
    {"country": "United Kingdom", "city": "London", "ip": "203.0.113.89"},
    {"country": "Germany", "city": "Berlin", "ip": "198.51.100.203"},
    {"country": "Japan", "city": "Tokyo", "ip": "203.0.113.100"},
    {"country": "Australia", "city": "Sydney", "ip": "198.51.100.250"},
]

DEVICE_IDS = ["DEV-001", "DEV-002", "DEV-003", "DEV-004", "DEV-005"]
APPS = ["Microsoft Office 365", "Azure Portal", "SharePoint Online", "Teams", "Outlook"]

OAUTH_APPS = ["ThirdPartyAnalytics", "CloudBackupService", "MarketingAutomation", "LegacyIntegration"]
HIGH_RISK_SCOPES = ["Mail.Read", "Files.Read.All", "offline_access", "User.ReadWrite.All", "Directory.ReadWrite.All"]
LOW_RISK_SCOPES = ["User.Read", "openid", "profile"]

ROLES = ["Global Administrator", "Security Administrator", "User Administrator", "Billing Administrator", "Exchange Administrator"]


def create_detections():
    """Create detection rules"""
    detections = [
        {
            "detection_id": "DET-001",
            "name": "MFA Fatigue Attack",
            "description": "Detects when a user receives an excessive number of MFA prompts within a short time window, followed by a successful authentication",
            "required_signals": json.dumps(["mfa_required=true", "mfa_result=fail/timeout", "sign_in_result=success"]),
            "detection_logic": "Count MFA prompts for same user within 10-30 minute window. If 6+ prompts with failures/timeouts followed by 1 success, trigger alert.",
            "expected_false_positives": "Users with legitimate connectivity issues may trigger false positives. Tune threshold based on baseline.",
            "severity": SeverityLevel.HIGH,
            "recommended_response": "1. Disable user account immediately 2. Revoke all active sessions 3. Require password reset 4. Review user's recent activity",
            "mitre_tactic": "Initial Access",
            "mitre_technique": "Multi-Factor Authentication Request Generation",
            "mitre_technique_id": "T1110.001"
        },
        {
            "detection_id": "DET-002",
            "name": "Impossible Travel",
            "description": "Detects when a user successfully authenticates from two geographically distant locations within an impossible time frame",
            "required_signals": json.dumps(["sign_in_result=success", "geo_country", "geo_city", "timestamp"]),
            "detection_logic": "Calculate distance and time between two successful sign-ins. If distance > 500 miles and time < 60 minutes, trigger alert.",
            "expected_false_positives": "VPN usage, legitimate travel, or shared accounts may cause false positives. Verify with user before action.",
            "severity": SeverityLevel.HIGH,
            "recommended_response": "1. Verify with user if travel is legitimate 2. If not, disable account and revoke sessions 3. Investigate IP addresses",
            "mitre_tactic": "Initial Access",
            "mitre_technique": "Valid Accounts",
            "mitre_technique_id": "T1078"
        },
        {
            "detection_id": "DET-003",
            "name": "Legacy Authentication Usage",
            "description": "Detects sign-ins using legacy authentication protocols that bypass MFA",
            "required_signals": json.dumps(["app_name=legacy", "sign_in_result=success", "mfa_required=false"]),
            "detection_logic": "If sign-in uses legacy protocol (IMAP, POP3, SMTP, ActiveSync) and MFA is not required, trigger alert.",
            "expected_false_positives": "Legitimate service accounts may use legacy auth. Whitelist known service accounts.",
            "severity": SeverityLevel.MEDIUM,
            "recommended_response": "1. Review if legacy auth is necessary 2. Enable MFA for legacy protocols 3. Consider blocking legacy auth",
            "mitre_tactic": "Defense Evasion",
            "mitre_technique": "Disable or Modify Security Tools",
            "mitre_technique_id": "T1562.001"
        },
        {
            "detection_id": "DET-004",
            "name": "Risky Sign-In with High Risk",
            "description": "Detects successful sign-ins that Azure AD Identity Protection flagged as high risk",
            "required_signals": json.dumps(["risk_level=high", "sign_in_result=success"]),
            "detection_logic": "If risk_level is 'high' and sign_in_result is 'success', trigger alert.",
            "expected_false_positives": "New device or location may trigger false positives. Review risk factors.",
            "severity": SeverityLevel.HIGH,
            "recommended_response": "1. Require MFA challenge 2. Review sign-in details 3. Check for suspicious activity",
            "mitre_tactic": "Initial Access",
            "mitre_technique": "Valid Accounts",
            "mitre_technique_id": "T1078"
        },
        {
            "detection_id": "DET-005",
            "name": "OAuth App Consent with High-Risk Scopes",
            "description": "Detects when a new OAuth application is consented with high-risk permissions",
            "required_signals": json.dumps(["oauth_app_name", "oauth_scopes"]),
            "detection_logic": "If new OAuth app consent includes high-risk scopes (Mail.Read, Files.Read.All, User.ReadWrite.All, Directory.ReadWrite.All), trigger alert.",
            "expected_false_positives": "Legitimate business applications may require high-risk scopes. Verify with business owner.",
            "severity": SeverityLevel.MEDIUM,
            "recommended_response": "1. Review OAuth app legitimacy 2. Verify consent was authorized 3. Revoke consent if suspicious 4. Block app if malicious",
            "mitre_tactic": "Persistence",
            "mitre_technique": "Cloud Accounts",
            "mitre_technique_id": "T1078.004"
        },
        {
            "detection_id": "DET-006",
            "name": "Privileged Role Assignment Outside Business Hours",
            "description": "Detects when a privileged role is assigned outside normal business hours or change windows",
            "required_signals": json.dumps(["role_assigned=true", "role_name", "timestamp"]),
            "detection_logic": "If privileged role (Global Admin, Security Admin, etc.) is assigned outside 8 AM - 6 PM on weekdays, trigger alert.",
            "expected_false_positives": "Emergency changes or global teams may cause false positives. Verify with change management.",
            "severity": SeverityLevel.HIGH,
            "recommended_response": "1. Verify role assignment is authorized 2. Review who made the change 3. Revoke if unauthorized 4. Investigate user activity",
            "mitre_tactic": "Privilege Escalation",
            "mitre_technique": "Cloud Account",
            "mitre_technique_id": "T1078.004"
        },
        {
            "detection_id": "DET-007",
            "name": "Azure Resource Creation from Unusual Location",
            "description": "Detects Azure resource creation from unusual geographic locations",
            "required_signals": json.dumps(["azure_activity=resource_create", "geo_country"]),
            "detection_logic": "If Azure resource is created from a country not in the allowed list, trigger alert.",
            "expected_false_positives": "Global teams may create resources from various locations. Maintain allow list.",
            "severity": SeverityLevel.MEDIUM,
            "recommended_response": "1. Verify resource creation is authorized 2. Review resource configuration 3. Delete if unauthorized",
            "mitre_tactic": "Impact",
            "mitre_technique": "Resource Hijacking",
            "mitre_technique_id": "T1496"
        },
        {
            "detection_id": "DET-008",
            "name": "Suspicious Policy Change",
            "description": "Detects suspicious Azure policy changes that could weaken security posture",
            "required_signals": json.dumps(["azure_activity=policy_change", "user"]),
            "detection_logic": "If policy change occurs outside change window or by non-authorized user, trigger alert.",
            "expected_false_positives": "Legitimate policy updates may occur. Verify with change management.",
            "severity": SeverityLevel.HIGH,
            "recommended_response": "1. Review policy change details 2. Verify authorization 3. Revert if unauthorized 4. Investigate who made change",
            "mitre_tactic": "Defense Evasion",
            "mitre_technique": "Disable or Modify Security Tools",
            "mitre_technique_id": "T1562.001"
        }
    ]

    for det_data in detections:
        detection = Detection(**det_data)
        db.add(detection)
    
    db.commit()
    print(f"Created {len(detections)} detection rules")


def generate_mfa_fatigue_scenario():
    """Generate MFA Fatigue attack scenario"""
    user = random.choice(USERS)
    base_time = datetime.utcnow() - timedelta(hours=2)
    ip = random.choice(IP_ADDRESSES)
    geo = random.choice(GEO_LOCATIONS)
    
    events = []
    
    # Generate 8-15 failed MFA prompts
    num_prompts = random.randint(8, 15)
    for i in range(num_prompts):
        event = SecurityEvent(
            timestamp=base_time + timedelta(minutes=i*2),
            user=user,
            ip_address=ip,
            geo_country=geo["country"],
            geo_city=geo["city"],
            device_id=random.choice(DEVICE_IDS),
            device_compliance="Compliant",
            app_name=random.choice(APPS),
            sign_in_result=SignInResult.FAIL,
            mfa_required=True,
            mfa_result=random.choice([MFAResult.FAIL, MFAResult.TIMEOUT]),
            risk_level=RiskLevel.MEDIUM,
            scenario_type="mfa_fatigue",
            detection_triggered=False
        )
        events.append(event)
    
    # Final successful sign-in
    success_event = SecurityEvent(
        timestamp=base_time + timedelta(minutes=num_prompts*2 + 1),
        user=user,
        ip_address=ip,
        geo_country=geo["country"],
        geo_city=geo["city"],
        device_id=random.choice(DEVICE_IDS),
        device_compliance="Compliant",
        app_name=random.choice(APPS),
        sign_in_result=SignInResult.SUCCESS,
        mfa_required=True,
        mfa_result=MFAResult.PASS,
        risk_level=RiskLevel.HIGH,
        alert_name="MFA Fatigue Attack Detected",
        alert_severity=SeverityLevel.HIGH,
        mitre_tactic="Initial Access",
        mitre_technique="Multi-Factor Authentication Request Generation",
        detection_id="DET-001",
        detection_triggered=True,
        scenario_type="mfa_fatigue"
    )
    events.append(success_event)
    
    # Create alert
    alert = Alert(
        alert_name="MFA Fatigue Attack Detected",
        severity=SeverityLevel.HIGH,
        detection_id="DET-001",
        user=user,
        ip_address=ip,
        timestamp=success_event.timestamp,
        scenario_type="mfa_fatigue",
        mitre_tactic="Initial Access",
        mitre_technique="Multi-Factor Authentication Request Generation"
    )
    db.add(alert)
    
    # Create incident
    incident = Incident(
        incident_id=f"INC-{random.randint(1000, 9999)}",
        title=f"MFA Fatigue Attack - {user}",
        description=f"User {user} received {num_prompts} MFA prompts with failures/timeouts, followed by successful authentication",
        severity=SeverityLevel.HIGH,
        status=IncidentStatus.OPEN,
        scenario_type="mfa_fatigue",
        user=user,
        detection_id="DET-001",
        detected_at=success_event.timestamp,
        mttd_minutes=random.uniform(5, 15)
    )
    db.add(incident)
    
    for event in events:
        db.add(event)
    
    db.commit()
    print(f"Generated MFA Fatigue scenario for {user} with {len(events)} events")


def generate_impossible_travel_scenario():
    """Generate Impossible Travel attack scenario"""
    user = random.choice(USERS)
    base_time = datetime.utcnow() - timedelta(hours=1)
    
    # First location (e.g., New York)
    loc1 = GEO_LOCATIONS[0]
    event1 = SecurityEvent(
        timestamp=base_time,
        user=user,
        ip_address=loc1["ip"],
        geo_country=loc1["country"],
        geo_city=loc1["city"],
        device_id=random.choice(DEVICE_IDS),
        device_compliance="Compliant",
        app_name=random.choice(APPS),
        sign_in_result=SignInResult.SUCCESS,
        mfa_required=True,
        mfa_result=MFAResult.PASS,
        risk_level=RiskLevel.LOW,
        scenario_type="impossible_travel",
        detection_triggered=False
    )
    db.add(event1)
    
    # Second location far away (e.g., Tokyo) within 30 minutes
    loc2 = GEO_LOCATIONS[4]  # Tokyo
    event2 = SecurityEvent(
        timestamp=base_time + timedelta(minutes=random.randint(15, 30)),
        user=user,
        ip_address=loc2["ip"],
        geo_country=loc2["country"],
        geo_city=loc2["city"],
        device_id=random.choice(DEVICE_IDS),
        device_compliance="Compliant",
        app_name=random.choice(APPS),
        sign_in_result=SignInResult.SUCCESS,
        mfa_required=True,
        mfa_result=MFAResult.PASS,
        risk_level=RiskLevel.HIGH,
        alert_name="Impossible Travel Detected",
        alert_severity=SeverityLevel.HIGH,
        mitre_tactic="Initial Access",
        mitre_technique="Valid Accounts",
        detection_id="DET-002",
        detection_triggered=True,
        scenario_type="impossible_travel"
    )
    db.add(event2)
    
    # Create alert
    alert = Alert(
        alert_name="Impossible Travel Detected",
        severity=SeverityLevel.HIGH,
        detection_id="DET-002",
        user=user,
        ip_address=loc2["ip"],
        timestamp=event2.timestamp,
        scenario_type="impossible_travel",
        mitre_tactic="Initial Access",
        mitre_technique="Valid Accounts"
    )
    db.add(alert)
    
    # Create incident
    incident = Incident(
        incident_id=f"INC-{random.randint(1000, 9999)}",
        title=f"Impossible Travel - {user}",
        description=f"User {user} authenticated from {loc1['city']}, {loc1['country']} and then {loc2['city']}, {loc2['country']} within 30 minutes",
        severity=SeverityLevel.HIGH,
        status=IncidentStatus.OPEN,
        scenario_type="impossible_travel",
        user=user,
        detection_id="DET-002",
        detected_at=event2.timestamp,
        mttd_minutes=random.uniform(10, 25)
    )
    db.add(incident)
    
    db.commit()
    print(f"Generated Impossible Travel scenario for {user}")


def generate_oauth_consent_abuse_scenario():
    """Generate OAuth Consent Abuse scenario"""
    user = random.choice(USERS)
    base_time = datetime.utcnow() - timedelta(hours=3)
    geo = random.choice(GEO_LOCATIONS)
    app_name = random.choice(OAUTH_APPS)
    scopes = ", ".join(random.sample(HIGH_RISK_SCOPES, 3))
    
    event = SecurityEvent(
        timestamp=base_time,
        user=user,
        ip_address=geo["ip"],
        geo_country=geo["country"],
        geo_city=geo["city"],
        device_id=random.choice(DEVICE_IDS),
        oauth_app_name=app_name,
        oauth_scopes=scopes,
        risk_level=RiskLevel.MEDIUM,
        alert_name="OAuth App Consent with High-Risk Scopes",
        alert_severity=SeverityLevel.MEDIUM,
        mitre_tactic="Persistence",
        mitre_technique="Cloud Accounts",
        detection_id="DET-005",
        detection_triggered=True,
        scenario_type="oauth_abuse"
    )
    db.add(event)
    
    # Create alert
    alert = Alert(
        alert_name="OAuth App Consent with High-Risk Scopes",
        severity=SeverityLevel.MEDIUM,
        detection_id="DET-005",
        user=user,
        ip_address=geo["ip"],
        timestamp=base_time,
        scenario_type="oauth_abuse",
        mitre_tactic="Persistence",
        mitre_technique="Cloud Accounts"
    )
    db.add(alert)
    
    # Create incident
    incident = Incident(
        incident_id=f"INC-{random.randint(1000, 9999)}",
        title=f"OAuth Consent Abuse - {app_name}",
        description=f"User {user} consented to OAuth app '{app_name}' with high-risk scopes: {scopes}",
        severity=SeverityLevel.MEDIUM,
        status=IncidentStatus.OPEN,
        scenario_type="oauth_abuse",
        user=user,
        detection_id="DET-005",
        detected_at=base_time,
        mttd_minutes=random.uniform(15, 45)
    )
    db.add(incident)
    
    db.commit()
    print(f"Generated OAuth Consent Abuse scenario for {user} with app {app_name}")


def generate_privilege_escalation_scenario():
    """Generate Privilege Escalation scenario"""
    user = random.choice(USERS)
    # Outside business hours (e.g., 2 AM)
    base_time = datetime.utcnow().replace(hour=2, minute=0, second=0) - timedelta(days=1)
    geo = random.choice(GEO_LOCATIONS)
    role = random.choice(ROLES)
    
    # Role assignment event
    event1 = SecurityEvent(
        timestamp=base_time,
        user=user,
        ip_address=geo["ip"],
        geo_country=geo["country"],
        geo_city=geo["city"],
        role_assigned=True,
        role_name=role,
        risk_level=RiskLevel.HIGH,
        alert_name="Privileged Role Assigned Outside Business Hours",
        alert_severity=SeverityLevel.HIGH,
        mitre_tactic="Privilege Escalation",
        mitre_technique="Cloud Account",
        detection_id="DET-006",
        detection_triggered=True,
        scenario_type="privilege_escalation"
    )
    db.add(event1)
    
    # Follow-up suspicious activity
    event2 = SecurityEvent(
        timestamp=base_time + timedelta(minutes=10),
        user=user,
        ip_address=geo["ip"],
        geo_country=geo["country"],
        geo_city=geo["city"],
        azure_activity=AzureActivityType.POLICY_CHANGE,
        risk_level=RiskLevel.HIGH,
        scenario_type="privilege_escalation",
        detection_triggered=False
    )
    db.add(event2)
    
    # Create alert
    alert = Alert(
        alert_name="Privileged Role Assigned Outside Business Hours",
        severity=SeverityLevel.HIGH,
        detection_id="DET-006",
        user=user,
        ip_address=geo["ip"],
        timestamp=base_time,
        scenario_type="privilege_escalation",
        mitre_tactic="Privilege Escalation",
        mitre_technique="Cloud Account"
    )
    db.add(alert)
    
    # Create incident
    incident = Incident(
        incident_id=f"INC-{random.randint(1000, 9999)}",
        title=f"Privilege Escalation - {role} assigned to {user}",
        description=f"User {user} was assigned privileged role '{role}' outside business hours, followed by suspicious policy changes",
        severity=SeverityLevel.HIGH,
        status=IncidentStatus.OPEN,
        scenario_type="privilege_escalation",
        user=user,
        detection_id="DET-006",
        detected_at=base_time,
        mttd_minutes=random.uniform(20, 60)
    )
    db.add(incident)
    
    db.commit()
    print(f"Generated Privilege Escalation scenario for {user} with role {role}")


def generate_normal_events():
    """Generate normal baseline events"""
    base_time = datetime.utcnow() - timedelta(days=7)
    
    for i in range(200):  # 200 normal events
        user = random.choice(USERS)
        geo = random.choice(GEO_LOCATIONS)
        event = SecurityEvent(
            timestamp=base_time + timedelta(hours=i*0.8),
            user=user,
            ip_address=geo["ip"],
            geo_country=geo["country"],
            geo_city=geo["city"],
            device_id=random.choice(DEVICE_IDS),
            device_compliance=random.choice(["Compliant", "NonCompliant"]),
            app_name=random.choice(APPS),
            sign_in_result=random.choice([SignInResult.SUCCESS, SignInResult.FAIL]),
            mfa_required=random.choice([True, False]),
            mfa_result=random.choice([MFAResult.PASS, MFAResult.FAIL]) if random.choice([True, False]) else None,
            risk_level=random.choice([RiskLevel.LOW, RiskLevel.MEDIUM]),
            scenario_type="normal",
            detection_triggered=False
        )
        db.add(event)
    
    db.commit()
    print("Generated 200 normal baseline events")


if __name__ == "__main__":
    print("Generating Detection Engineering Simulation data...")
    print("=" * 60)
    
    # Clear existing data
    db.query(SecurityEvent).delete()
    db.query(Detection).delete()
    db.query(Alert).delete()
    db.query(Incident).delete()
    db.commit()
    
    # Create detections
    create_detections()
    
    # Generate attack scenarios (multiple instances)
    print("\nGenerating attack scenarios...")
    for _ in range(3):
        generate_mfa_fatigue_scenario()
    for _ in range(2):
        generate_impossible_travel_scenario()
    for _ in range(2):
        generate_oauth_consent_abuse_scenario()
    for _ in range(2):
        generate_privilege_escalation_scenario()
    
    # Generate normal events
    print("\nGenerating normal baseline events...")
    generate_normal_events()
    
    print("\n" + "=" * 60)
    print("Data generation complete!")
    print(f"Total events: {db.query(SecurityEvent).count()}")
    print(f"Total alerts: {db.query(Alert).count()}")
    print(f"Total incidents: {db.query(Incident).count()}")
    print(f"Total detections: {db.query(Detection).count()}")
    
    db.close()
