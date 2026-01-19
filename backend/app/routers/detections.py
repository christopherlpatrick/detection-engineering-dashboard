"""
Detection rules API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.models import get_db, Detection, SecurityEvent, Alert
from app.schemas import DetectionSchema

router = APIRouter()


@router.get("/detections")
async def get_detections(db: Session = Depends(get_db)):
    """Get all detection rules"""
    detections = db.query(Detection).all()
    return [
        {c.name: getattr(d, c.name) for c in d.__table__.columns}
        for d in detections
    ]


@router.get("/detections/{detection_id}")
async def get_detection(detection_id: str, db: Session = Depends(get_db)):
    """Get a specific detection rule"""
    detection = db.query(Detection).filter(Detection.detection_id == detection_id).first()
    if not detection:
        return {"error": "Detection not found"}
    
    # Get example events that triggered this detection
    example_events = db.query(SecurityEvent).filter(
        SecurityEvent.detection_id == detection_id,
        SecurityEvent.detection_triggered == True
    ).limit(5).all()
    
    # Get alert count
    alert_count = db.query(Alert).filter(Alert.detection_id == detection_id).count()
    
    result = {c.name: getattr(detection, c.name) for c in detection.__table__.columns}
    # Convert enum values to strings
    if hasattr(detection, 'severity') and detection.severity:
        result['severity'] = detection.severity.value if hasattr(detection.severity, 'value') else str(detection.severity)
    return {
        **result,
        "example_events": [
            {
                "id": e.id,
                "timestamp": e.timestamp.isoformat(),
                "user": e.user,
                "scenario_type": e.scenario_type
            }
            for e in example_events
        ],
        "alert_count": alert_count
    }
