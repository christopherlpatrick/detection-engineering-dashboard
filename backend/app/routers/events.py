"""
Security events API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from typing import Optional
from app.models import get_db, SecurityEvent

router = APIRouter()


@router.get("/events")
async def get_events(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    user: Optional[str] = Query(None),
    scenario_type: Optional[str] = Query(None),
    detection_triggered: Optional[bool] = Query(None),
    limit: int = Query(100),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """Get security events with filters"""
    filters = []
    
    if start_date:
        filters.append(SecurityEvent.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        filters.append(SecurityEvent.timestamp <= datetime.fromisoformat(end_date))
    if user:
        filters.append(SecurityEvent.user == user)
    if scenario_type:
        filters.append(SecurityEvent.scenario_type == scenario_type)
    if detection_triggered is not None:
        filters.append(SecurityEvent.detection_triggered == detection_triggered)
    
    events = db.query(SecurityEvent).filter(*filters).order_by(
        SecurityEvent.timestamp.desc()
    ).offset(offset).limit(limit).all()
    
    total = db.query(SecurityEvent).filter(*filters).count()
    
    return {
        "events": [
            {c.name: getattr(e, c.name) for c in e.__table__.columns}
            for e in events
        ],
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.get("/events/timeline")
async def get_timeline_events(
    scenario_type: Optional[str] = Query(None),
    user: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get events for timeline view, grouped by scenario"""
    filters = []
    if scenario_type:
        filters.append(SecurityEvent.scenario_type == scenario_type)
    if user:
        filters.append(SecurityEvent.user == user)
    
    events = db.query(SecurityEvent).filter(*filters).order_by(
        SecurityEvent.timestamp.asc()
    ).all()
    
    timeline = []
    for event in events:
        # Determine event type based on detection and scenario
        if event.detection_triggered:
            event_type = "detection"
        elif event.scenario_type and event.scenario_type != "normal":
            event_type = "attack"
        else:
            event_type = "pre_attack"
        
        timeline.append({
            "id": event.id,
            "timestamp": event.timestamp.isoformat(),
            "event_type": event_type,
            "description": f"{event.user} - {event.scenario_type or 'normal activity'}",
            "user": event.user,
            "detection_id": event.detection_id,
            "mitre_tactic": event.mitre_tactic,
            "mitre_technique": event.mitre_technique,
            "scenario_type": event.scenario_type
        })
    
    return timeline
