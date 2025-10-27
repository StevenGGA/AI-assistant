"""
Meeting schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class MeetingBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    project_id: int
    meeting_date: datetime
    duration_minutes: Optional[int] = Field(None, ge=0)
    location: Optional[str] = None
    raw_notes: Optional[str] = None


class MeetingCreate(MeetingBase):
    pass


class MeetingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    meeting_date: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    location: Optional[str] = None
    raw_notes: Optional[str] = None
    ai_summary: Optional[str] = None
    key_decisions: Optional[List[str]] = None
    action_items: Optional[List[Dict[str, Any]]] = None


class Meeting(MeetingBase):
    id: int
    creator_id: int
    ai_summary: Optional[str] = None
    key_decisions: Optional[List[str]] = None
    action_items: Optional[List[Dict[str, Any]]] = None
    google_doc_id: Optional[str] = None
    slack_thread_ts: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class WeeklyReport(BaseModel):
    id: int
    project_id: int
    week_number: int
    year: int
    tasks_completed: Optional[List[int]] = []
    tasks_in_progress: Optional[List[int]] = []
    tasks_planned: Optional[List[int]] = []
    completion_rate: Optional[int] = None
    hours_logged: Optional[int] = None
    summary: Optional[str] = None
    blockers: Optional[List[str]] = []
    highlights: Optional[List[str]] = []
    next_steps: Optional[List[str]] = []
    week_start: datetime
    week_end: datetime
    generated_at: datetime
    
    class Config:
        from_attributes = True