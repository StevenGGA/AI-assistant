"""
Integration schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class IntegrationType(str, Enum):
    GOOGLE_DRIVE = "google_drive"
    SLACK = "slack"
    CANVAS = "canvas"


class IntegrationStatus(BaseModel):
    type: IntegrationType
    connected: bool
    account_email: Optional[str] = None
    team_id: Optional[str] = None
    canvas_domain: Optional[str] = None
    last_sync: Optional[datetime] = None
    sync_status: Optional[str] = None


class IntegrationConnect(BaseModel):
    type: IntegrationType
    redirect_url: Optional[str] = None


class IntegrationCallback(BaseModel):
    code: str
    state: Optional[str] = None


class Integration(BaseModel):
    id: int
    user_id: int
    type: IntegrationType
    is_active: bool = True
    account_email: Optional[str] = None
    team_id: Optional[str] = None
    canvas_domain: Optional[str] = None
    last_sync: Optional[datetime] = None
    sync_status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    connected_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True