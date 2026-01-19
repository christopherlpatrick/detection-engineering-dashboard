"""
Incidents API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.models import get_db, Incident, Alert, IncidentStatus, SeverityLevel
import json

router = APIRouter()


@router.get("/incidents")
async def get_incidents(
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    scenario_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all incidents with optional filters"""
    filters = []
    if status:
        # Convert string to enum if needed
        try:
            status_enum = IncidentStatus[status.upper()]
            filters.append(Incident.status == status_enum)
        except:
            # Try as value instead
            try:
                status_enum = IncidentStatus(status.lower())
                filters.append(Incident.status == status_enum)
            except:
                filters.append(Incident.status == status)
    if severity:
        try:
            severity_enum = SeverityLevel[severity.upper()]
            filters.append(Incident.severity == severity_enum)
        except:
            filters.append(Incident.severity == severity)
    if scenario_type:
        filters.append(Incident.scenario_type == scenario_type)
    
    incidents = db.query(Incident).filter(*filters).order_by(
        Incident.detected_at.desc()
    ).all()
    
    # Convert enum values to strings for JSON serialization
    result = []
    for i in incidents:
        item = {}
        for c in i.__table__.columns:
            value = getattr(i, c.name)
            # Convert enum to string
            if hasattr(value, 'value'):
                item[c.name] = value.value
            elif hasattr(value, 'name'):
                item[c.name] = value.name
            else:
                item[c.name] = value
        result.append(item)
    
    return result


@router.get("/incidents/{incident_id}")
async def get_incident(incident_id: str, db: Session = Depends(get_db)):
    """Get a specific incident"""
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        return {"error": "Incident not found"}
    
    # Convert enum values to strings
    result = {}
    for c in incident.__table__.columns:
        value = getattr(incident, c.name)
        if hasattr(value, 'value'):
            result[c.name] = value.value
        elif hasattr(value, 'name'):
            result[c.name] = value.name
        else:
            result[c.name] = value
    return result


@router.get("/users/{user}/investigation")
async def get_user_investigation(user: str, db: Session = Depends(get_db)):
    """Get comprehensive investigation data for a user"""
    from app.models import SecurityEvent
    
    # Get all events for user
    events = db.query(SecurityEvent).filter(
        SecurityEvent.user == user
    ).order_by(SecurityEvent.timestamp.desc()).all()
    
    # Get alerts for user
    alerts = db.query(Alert).filter(
        Alert.user == user
    ).order_by(Alert.timestamp.desc()).all()
    
    # Get incidents for user
    incidents = db.query(Incident).filter(
        Incident.user == user
    ).order_by(Incident.detected_at.desc()).all()
    
    # Extract unique IPs, devices, apps, OAuth apps
    unique_ips = list(set([e.ip_address for e in events if e.ip_address]))
    unique_devices = list(set([e.device_id for e in events if e.device_id]))
    unique_apps = list(set([e.app_name for e in events if e.app_name]))
    unique_oauth = list(set([e.oauth_app_name for e in events if e.oauth_app_name]))
    
    # Get role changes
    role_changes = [e for e in events if e.role_assigned]
    
    # Get OAuth consents
    oauth_consents = [e for e in events if e.oauth_app_name]
    
    # Get geolocation changes
    geo_changes = []
    seen_locations = set()
    for e in events:
        if e.geo_country and e.geo_city:
            loc_key = f"{e.geo_country}-{e.geo_city}"
            if loc_key not in seen_locations:
                geo_changes.append({
                    "country": e.geo_country,
                    "city": e.geo_city,
                    "timestamp": e.timestamp.isoformat(),
                    "ip_address": e.ip_address
                })
                seen_locations.add(loc_key)
    
    def serialize_item(item):
        """Convert database item to dict, handling enums"""
        result = {}
        for c in item.__table__.columns:
            value = getattr(item, c.name)
            if hasattr(value, 'value'):
                result[c.name] = value.value
            elif hasattr(value, 'name'):
                result[c.name] = value.name
            else:
                result[c.name] = value
        return result
    
    return {
        "user": user,
        "events": [serialize_item(e) for e in events],
        "alerts": [serialize_item(a) for a in alerts],
        "incidents": [serialize_item(i) for i in incidents],
        "unique_ips": unique_ips,
        "unique_devices": unique_devices,
        "unique_apps": unique_apps,
        "unique_oauth_apps": unique_oauth,
        "role_changes": [
            {
                "timestamp": e.timestamp.isoformat(),
                "role_name": e.role_name,
                "ip_address": e.ip_address
            }
            for e in role_changes
        ],
        "oauth_consents": [
            {
                "timestamp": e.timestamp.isoformat(),
                "app_name": e.oauth_app_name,
                "scopes": e.oauth_scopes,
                "ip_address": e.ip_address
            }
            for e in oauth_consents
        ],
        "geolocation_changes": geo_changes
    }
