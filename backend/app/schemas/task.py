"""
Task schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: Optional[int] = None
    estimated_hours: Optional[int] = Field(None, ge=0)
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    project_id: int
    meeting_id: Optional[int] = None  # If extracted from meeting
    ai_extracted: Optional[str] = None  # Original AI extraction
    ai_confidence: Optional[int] = Field(None, ge=0, le=100)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[int] = None
    estimated_hours: Optional[int] = Field(None, ge=0)
    actual_hours: Optional[int] = Field(None, ge=0)
    due_date: Optional[datetime] = None


class Task(TaskBase):
    id: int
    project_id: int
    creator_id: int
    meeting_id: Optional[int] = None
    actual_hours: Optional[int] = None
    completed_at: Optional[datetime] = None
    ai_extracted: Optional[str] = None
    ai_confidence: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Related info
    assignee_name: Optional[str] = None
    creator_name: Optional[str] = None
    project_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class TaskBulkCreate(BaseModel):
    tasks: List[TaskCreate]


class TaskStats(BaseModel):
    total: int = 0
    todo: int = 0
    in_progress: int = 0
    review: int = 0
    done: int = 0
    blocked: int = 0
    cancelled: int = 0
    completion_rate: float = 0.0