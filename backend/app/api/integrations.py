"""
Integrations API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.auth import get_current_active_user

router = APIRouter()


@router.get("/")
def get_integrations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's integrations"""
    return {
        "google_drive": bool(current_user.google_token),
        "slack": bool(current_user.slack_token),
        "canvas": bool(current_user.canvas_token)
    }


@router.post("/{integration_type}/connect")
def connect_integration(
    integration_type: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Connect an integration"""
    return {"message": f"Connect {integration_type} - OAuth flow to be implemented"}


@router.delete("/{integration_type}")
def disconnect_integration(
    integration_type: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Disconnect an integration"""
    return {"message": f"Disconnect {integration_type} - to be implemented"}