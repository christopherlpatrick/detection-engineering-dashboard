"""
Response actions API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import get_db, Incident, ResponseAction, IncidentStatus

router = APIRouter()


@router.post("/incidents/{incident_id}/response/{action_type}")
async def execute_response_action(
    incident_id: str,
    action_type: str,
    db: Session = Depends(get_db)
):
    """Execute a simulated response action"""
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        return {"error": "Incident not found"}
    
    action_descriptions = {
        "disable_user": {
            "name": "Disable User Account",
            "description": "In production, this would disable the user account in Azure AD, preventing all future sign-ins. The user would need admin intervention to re-enable the account."
        },
        "revoke_sessions": {
            "name": "Revoke All Active Sessions",
            "description": "In production, this would invalidate all active tokens and sessions for the user, forcing them to re-authenticate. This would immediately log them out of all devices and applications."
        },
        "password_reset": {
            "name": "Require Password Reset",
            "description": "In production, this would force the user to reset their password on next sign-in. This helps ensure the account hasn't been compromised and the password is changed."
        },
        "isolate_endpoint": {
            "name": "Isolate Endpoint",
            "description": "In production, this would isolate the device from the network, preventing it from accessing corporate resources while allowing investigation. This is typically done via Microsoft Defender for Endpoint or similar EDR solution."
        },
        "block_oauth": {
            "name": "Block OAuth Application",
            "description": "In production, this would revoke consent and block the OAuth application, preventing it from accessing user data. This would also revoke all existing tokens issued to the application."
        }
    }
    
    if action_type not in action_descriptions:
        return {"error": "Invalid action type"}
    
    action_info = action_descriptions[action_type]
    
    # Create response action record
    response_action = ResponseAction(
        incident_id=incident_id,
        action_type=action_type,
        action_name=action_info["name"],
        description=action_info["description"],
        simulated=True,
        executed_at=datetime.utcnow()
    )
    db.add(response_action)
    
    # Update incident status
    if incident.status == IncidentStatus.OPEN:
        incident.status = IncidentStatus.INVESTIGATING
        incident.acknowledged_at = datetime.utcnow()
    elif incident.status == IncidentStatus.INVESTIGATING:
        incident.status = IncidentStatus.CONTAINED
        incident.contained_at = datetime.utcnow()
    elif incident.status == IncidentStatus.CONTAINED:
        incident.status = IncidentStatus.RESOLVED
        incident.resolved_at = datetime.utcnow()
        # Calculate MTTR
        if incident.detected_at:
            mttr = (datetime.utcnow() - incident.detected_at).total_seconds() / 60
            incident.mttr_minutes = mttr
    
    # Update response_actions JSON
    existing_actions = incident.response_actions or "[]"
    import json
    try:
        actions_list = json.loads(existing_actions)
    except:
        actions_list = []
    
    actions_list.append({
        "action_type": action_type,
        "action_name": action_info["name"],
        "executed_at": datetime.utcnow().isoformat()
    })
    incident.response_actions = json.dumps(actions_list)
    
    db.commit()
    
    return {
        "success": True,
        "action": action_info,
        "incident_status": incident.status.value,
        "message": f"Simulated action executed. {action_info['description']}"
    }


@router.get("/incidents/{incident_id}/response-actions")
async def get_response_actions(incident_id: str, db: Session = Depends(get_db)):
    """Get all response actions for an incident"""
    actions = db.query(ResponseAction).filter(
        ResponseAction.incident_id == incident_id
    ).order_by(ResponseAction.executed_at.desc()).all()
    
    return [
        {c.name: getattr(a, c.name) for c in a.__table__.columns}
        for a in actions
    ]
