"""
Meetings API endpoints
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.auth import get_current_active_user

router = APIRouter()


@router.get("/")
def get_meetings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get meetings for user's projects"""
    return {"message": "Meetings endpoint - to be implemented"}


@router.post("/")
def create_meeting(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new meeting"""
    return {"message": "Create meeting - to be implemented"}