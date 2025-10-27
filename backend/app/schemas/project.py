"""
Project schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ProjectStatus(str, Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"


class MemberRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    google_drive_folder_id: Optional[str] = None
    slack_channel_id: Optional[str] = None
    canvas_course_id: Optional[str] = None


class ProjectMemberBase(BaseModel):
    user_id: int
    role: MemberRole = MemberRole.MEMBER


class ProjectMember(ProjectMemberBase):
    id: int
    project_id: int
    joined_at: datetime
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class Project(ProjectBase):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Integration IDs
    google_drive_folder_id: Optional[str] = None
    slack_channel_id: Optional[str] = None
    canvas_course_id: Optional[str] = None
    
    # Related counts
    member_count: Optional[int] = 0
    task_count: Optional[int] = 0
    meeting_count: Optional[int] = 0
    
    # Members list (optional)
    members: Optional[List[ProjectMember]] = []
    
    class Config:
        from_attributes = True


class AddProjectMember(BaseModel):
    user_id: int
    role: MemberRole = MemberRole.MEMBER


class UpdateProjectMember(BaseModel):
    role: MemberRole