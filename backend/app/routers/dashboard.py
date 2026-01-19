"""
Dashboard API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from typing import Optional
from app.models import get_db, SecurityEvent, Alert, Incident, Detection, RiskLevel, SeverityLevel
from app.schemas import DashboardKPISchema
from collections import Counter

router = APIRouter()


@router.get("/dashboard/kpis")
async def get_dashboard_kpis(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    user: Optional[str] = Query(None),
    scenario_type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get dashboard KPIs"""
    # Build filters
    filters = []
    if start_date:
        filters.append(SecurityEvent.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        filters.append(SecurityEvent.timestamp <= datetime.fromisoformat(end_date))
    if user:
        filters.append(SecurityEvent.user == user)
    if scenario_type:
        filters.append(SecurityEvent.scenario_type == scenario_type)
    
    # Get alerts with filters
    alert_filters = []
    if start_date:
        alert_filters.append(Alert.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        alert_filters.append(Alert.timestamp <= datetime.fromisoformat(end_date))
    if user:
        alert_filters.append(Alert.user == user)
    if scenario_type:
        alert_filters.append(Alert.scenario_type == scenario_type)
    if severity:
        # Convert string to enum if needed
        try:
            severity_enum = SeverityLevel[severity.upper()]
            alert_filters.append(Alert.severity == severity_enum)
        except:
            alert_filters.append(Alert.severity == severity)
    
    # Calculate KPIs
    total_alerts = db.query(Alert).filter(*alert_filters).count()
    # Handle enum comparison
    try:
        high_severity_alerts = db.query(Alert).filter(
            *alert_filters,
            Alert.severity.in_([SeverityLevel.HIGH, SeverityLevel.CRITICAL])
        ).count()
    except:
        # Fallback if enum comparison fails
        high_severity_alerts = db.query(Alert).filter(
            *alert_filters
        ).filter(
            or_(
                Alert.severity == 'high',
                Alert.severity == 'critical'
            )
        ).count()
    
    distinct_users = db.query(Alert.user).filter(
        *alert_filters,
        Alert.user.isnot(None)
    ).distinct().count()
    
    # Calculate MTTD and MTTR
    incidents = db.query(Incident).filter(
        Incident.detected_at.isnot(None)
    ).all()
    
    mttd_list = [inc.mttd_minutes for inc in incidents if inc.mttd_minutes is not None]
    mttd = sum(mttd_list) / len(mttd_list) if mttd_list else 0
    
    mttr_list = [inc.mttr_minutes for inc in incidents if inc.mttr_minutes is not None]
    mttr = sum(mttr_list) / len(mttr_list) if mttr_list else 0
    
    # Top MITRE tactics
    tactics = db.query(Alert.mitre_tactic).filter(
        *alert_filters,
        Alert.mitre_tactic.isnot(None)
    ).all()
    tactic_counts = Counter([t[0] for t in tactics if t[0]])
    top_tactics = [{"tactic": k, "count": v} for k, v in tactic_counts.most_common(5)]
    
    return {
        "total_alerts": total_alerts,
        "high_severity_alerts": high_severity_alerts,
        "distinct_impacted_users": distinct_users,
        "mttd_minutes": round(mttd, 2),
        "mttr_minutes": round(mttr, 2),
        "top_tactics": top_tactics
    }


@router.get("/dashboard/alert-trends")
async def get_alert_trends(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get alert trends over time"""
    filters = []
    if start_date:
        filters.append(Alert.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        filters.append(Alert.timestamp <= datetime.fromisoformat(end_date))
    else:
        # Default to last 7 days
        filters.append(Alert.timestamp >= datetime.utcnow() - timedelta(days=7))
    
    alerts = db.query(
        func.date(Alert.timestamp).label('date'),
        func.count(Alert.id).label('count')
    ).filter(*filters).group_by(func.date(Alert.timestamp)).all()
    
    return [{"date": str(a.date), "count": a.count} for a in alerts]


@router.get("/dashboard/sign-in-stats")
async def get_sign_in_stats(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get sign-in success vs failure statistics"""
    filters = []
    if start_date:
        filters.append(SecurityEvent.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        filters.append(SecurityEvent.timestamp <= datetime.fromisoformat(end_date))
    else:
        filters.append(SecurityEvent.timestamp >= datetime.utcnow() - timedelta(days=7))
    
    success_count = db.query(SecurityEvent).filter(
        *filters,
        SecurityEvent.sign_in_result == "success"
    ).count()
    
    fail_count = db.query(SecurityEvent).filter(
        *filters,
        SecurityEvent.sign_in_result == "fail"
    ).count()
    
    return {
        "success": success_count,
        "fail": fail_count
    }


@router.get("/dashboard/mfa-stats")
async def get_mfa_stats(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get MFA success vs failure statistics"""
    filters = []
    if start_date:
        filters.append(SecurityEvent.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        filters.append(SecurityEvent.timestamp <= datetime.fromisoformat(end_date))
    else:
        filters.append(SecurityEvent.timestamp >= datetime.utcnow() - timedelta(days=7))
    
    pass_count = db.query(SecurityEvent).filter(
        *filters,
        SecurityEvent.mfa_result == "pass"
    ).count()
    
    fail_count = db.query(SecurityEvent).filter(
        *filters,
        SecurityEvent.mfa_result == "fail"
    ).count()
    
    timeout_count = db.query(SecurityEvent).filter(
        *filters,
        SecurityEvent.mfa_result == "timeout"
    ).count()
    
    return {
        "pass": pass_count,
        "fail": fail_count,
        "timeout": timeout_count
    }
