"""
Database models for Detection Engineering Simulation Dashboard
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, Text, Enum, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./detection_engineering.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class RiskLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SeverityLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SignInResult(enum.Enum):
    SUCCESS = "success"
    FAIL = "fail"


class MFAResult(enum.Enum):
    PASS = "pass"
    FAIL = "fail"
    TIMEOUT = "timeout"


class AzureActivityType(enum.Enum):
    RESOURCE_CREATE = "resource_create"
    RESOURCE_DELETE = "resource_delete"
    POLICY_CHANGE = "policy_change"


class IncidentStatus(enum.Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    RESOLVED = "resolved"


class SecurityEvent(Base):
    """Security event model with all required fields"""
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    user = Column(String(100), index=True)
    ip_address = Column(String(45), index=True)
    geo_country = Column(String(100), index=True)
    geo_city = Column(String(100))
    device_id = Column(String(100), index=True)
    device_compliance = Column(String(50))
    app_name = Column(String(200))
    sign_in_result = Column(Enum(SignInResult), index=True)
    mfa_required = Column(Boolean, default=False)
    mfa_result = Column(Enum(MFAResult))
    risk_level = Column(Enum(RiskLevel), index=True)
    oauth_app_name = Column(String(200))
    oauth_scopes = Column(Text)  # JSON string or comma-separated
    role_assigned = Column(Boolean, default=False)
    role_name = Column(String(100))
    azure_activity = Column(Enum(AzureActivityType))
    alert_name = Column(String(200))
    alert_severity = Column(Enum(SeverityLevel))
    mitre_tactic = Column(String(100))
    mitre_technique = Column(String(100))
    detection_id = Column(String(100), index=True)
    detection_triggered = Column(Boolean, default=False, index=True)
    scenario_type = Column(String(100), index=True)  # mfa_fatigue, impossible_travel, oauth_abuse, privilege_escalation
    created_at = Column(DateTime, default=datetime.utcnow)


class Detection(Base):
    """Detection rule model"""
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    detection_id = Column(String(100), unique=True, index=True)
    name = Column(String(200))
    description = Column(Text)
    required_signals = Column(Text)  # JSON array of required signals
    detection_logic = Column(Text)  # Plain English description
    expected_false_positives = Column(Text)
    severity = Column(Enum(SeverityLevel), index=True)
    recommended_response = Column(Text)
    mitre_tactic = Column(String(100))
    mitre_technique = Column(String(100))
    mitre_technique_id = Column(String(50))  # e.g., T1110.001
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    """Alert model"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_name = Column(String(200))
    severity = Column(Enum(SeverityLevel), index=True)
    detection_id = Column(String(100), ForeignKey("detections.detection_id"), index=True)
    user = Column(String(100), index=True)
    ip_address = Column(String(45))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    scenario_type = Column(String(100), index=True)
    mitre_tactic = Column(String(100))
    mitre_technique = Column(String(100))
    status = Column(String(50), default="new")  # new, investigating, resolved
    created_at = Column(DateTime, default=datetime.utcnow)


class Incident(Base):
    """Incident response model"""
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String(100), unique=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    severity = Column(Enum(SeverityLevel), index=True)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.OPEN, index=True)
    scenario_type = Column(String(100), index=True)
    user = Column(String(100), index=True)
    detection_id = Column(String(100))
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    detected_at = Column(DateTime, index=True)
    acknowledged_at = Column(DateTime, nullable=True)
    contained_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    mttd_minutes = Column(Float, nullable=True)  # Mean Time To Detect
    mttr_minutes = Column(Float, nullable=True)  # Mean Time To Respond
    response_actions = Column(Text)  # JSON array of actions taken
    created_at = Column(DateTime, default=datetime.utcnow)

    alert = relationship("Alert", foreign_keys=[alert_id])


class ResponseAction(Base):
    """Simulated response actions"""
    __tablename__ = "response_actions"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String(100), ForeignKey("incidents.incident_id"), index=True)
    action_type = Column(String(100))  # disable_user, revoke_sessions, password_reset, isolate_endpoint, block_oauth
    action_name = Column(String(200))
    description = Column(Text)
    simulated = Column(Boolean, default=True)
    executed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
