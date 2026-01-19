"""
Pydantic schemas for API requests/responses
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models import RiskLevel, SeverityLevel, SignInResult, MFAResult, AzureActivityType, IncidentStatus


class SecurityEventSchema(BaseModel):
    id: int
    timestamp: datetime
    user: str
    ip_address: str
    geo_country: str
    geo_city: Optional[str]
    device_id: Optional[str]
    device_compliance: Optional[str]
    app_name: Optional[str]
    sign_in_result: Optional[str]
    mfa_required: Optional[bool]
    mfa_result: Optional[str]
    risk_level: Optional[str]
    oauth_app_name: Optional[str]
    oauth_scopes: Optional[str]
    role_assigned: Optional[bool]
    role_name: Optional[str]
    azure_activity: Optional[str]
    alert_name: Optional[str]
    alert_severity: Optional[str]
    mitre_tactic: Optional[str]
    mitre_technique: Optional[str]
    detection_id: Optional[str]
    detection_triggered: bool
    scenario_type: Optional[str]

    class Config:
        from_attributes = True


class DetectionSchema(BaseModel):
    id: int
    detection_id: str
    name: str
    description: str
    required_signals: str
    detection_logic: str
    expected_false_positives: str
    severity: str
    recommended_response: str
    mitre_tactic: str
    mitre_technique: str
    mitre_technique_id: Optional[str]

    class Config:
        from_attributes = True


class AlertSchema(BaseModel):
    id: int
    alert_name: str
    severity: str
    detection_id: Optional[str]
    user: Optional[str]
    ip_address: Optional[str]
    timestamp: datetime
    scenario_type: Optional[str]
    mitre_tactic: Optional[str]
    mitre_technique: Optional[str]
    status: str

    class Config:
        from_attributes = True


class IncidentSchema(BaseModel):
    id: int
    incident_id: str
    title: str
    description: str
    severity: str
    status: str
    scenario_type: Optional[str]
    user: Optional[str]
    detection_id: Optional[str]
    alert_id: Optional[int]
    detected_at: datetime
    acknowledged_at: Optional[datetime]
    contained_at: Optional[datetime]
    resolved_at: Optional[datetime]
    mttd_minutes: Optional[float]
    mttr_minutes: Optional[float]
    response_actions: Optional[str]

    class Config:
        from_attributes = True


class DashboardKPISchema(BaseModel):
    total_alerts: int
    high_severity_alerts: int
    distinct_impacted_users: int
    mttd_minutes: float
    mttr_minutes: float
    top_tactics: List[dict]


class TimelineEventSchema(BaseModel):
    id: int
    timestamp: datetime
    event_type: str  # pre_attack, attack, detection, response
    description: str
    user: Optional[str]
    detection_id: Optional[str]
    mitre_tactic: Optional[str]
    mitre_technique: Optional[str]
    scenario_type: str

    class Config:
        from_attributes = True
