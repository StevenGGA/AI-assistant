"""
Projects API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.user import User
from app.models.project import Project, ProjectMember, MemberRole as MemberRoleModel
from app.schemas.project import (
    Project as ProjectSchema, 
    ProjectCreate, 
    ProjectUpdate,
    AddProjectMember,
    UpdateProjectMember,
    ProjectMember as ProjectMemberSchema
)
from app.utils.auth import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[ProjectSchema])
def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all projects for current user"""
    # Get projects where user is a member
    projects = db.query(Project).join(ProjectMember).filter(
        ProjectMember.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    # Add counts for each project
    for project in projects:
        project.member_count = db.query(ProjectMember).filter(
            ProjectMember.project_id == project.id
        ).count()
        project.task_count = len(project.tasks)
        project.meeting_count = len(project.meetings)
    
    return projects


@router.post("/", response_model=ProjectSchema)
def create_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new project"""
    # Create project
    db_project = Project(
        **project.dict(),
        creator_id=current_user.id
    )
    db.add(db_project)
    db.flush()  # Get the project ID without committing
    
    # Add creator as owner
    db_member = ProjectMember(
        project_id=db_project.id,
        user_id=current_user.id,
        role=MemberRoleModel.OWNER
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_project)
    
    return db_project


@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific project"""
    # Check if user has access to project
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project"
        )
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Add counts
    project.member_count = db.query(ProjectMember).filter(
        ProjectMember.project_id == project.id
    ).count()
    project.task_count = len(project.tasks)
    project.meeting_count = len(project.meetings)
    
    # Add members list
    members = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id
    ).all()
    
    project.members = []
    for m in members:
        member_data = ProjectMemberSchema(
            id=m.id,
            project_id=m.project_id,
            user_id=m.user_id,
            role=m.role.value,
            joined_at=m.joined_at,
            user_email=m.user.email,
            user_name=m.user.username
        )
        project.members.append(member_data)
    
    return project


@router.patch("/{project_id}", response_model=ProjectSchema)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a project (requires admin or owner role)"""
    # Check if user has admin/owner access
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
        ProjectMember.role.in_([MemberRoleModel.OWNER, MemberRoleModel.ADMIN])
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this project"
        )
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Update fields
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a project (requires owner role)"""
    # Check if user is owner
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
        ProjectMember.role == MemberRoleModel.OWNER
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project owner can delete the project"
        )
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}


@router.post("/{project_id}/members", response_model=ProjectMemberSchema)
def add_project_member(
    project_id: int,
    member_data: AddProjectMember,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a member to project (requires admin or owner role)"""
    # Check if current user has permission
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
        ProjectMember.role.in_([MemberRoleModel.OWNER, MemberRoleModel.ADMIN])
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to add members"
        )
    
    # Check if user exists
    new_user = db.query(User).filter(User.id == member_data.user_id).first()
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is already a member
    existing_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == member_data.user_id
    ).first()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this project"
        )
    
    # Add new member
    db_member = ProjectMember(
        project_id=project_id,
        user_id=member_data.user_id,
        role=getattr(MemberRoleModel, member_data.role.value.upper())
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    
    return ProjectMemberSchema(
        id=db_member.id,
        project_id=db_member.project_id,
        user_id=db_member.user_id,
        role=db_member.role.value,
        joined_at=db_member.joined_at,
        user_email=new_user.email,
        user_name=new_user.username
    )


@router.delete("/{project_id}/members/{member_id}")
def remove_project_member(
    project_id: int,
    member_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove a member from project"""
    # Check if current user has permission
    current_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
        ProjectMember.role.in_([MemberRoleModel.OWNER, MemberRoleModel.ADMIN])
    ).first()
    
    if not current_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to remove members"
        )
    
    # Get the member to remove
    member_to_remove = db.query(ProjectMember).filter(
        ProjectMember.id == member_id,
        ProjectMember.project_id == project_id
    ).first()
    
    if not member_to_remove:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # Can't remove the owner
    if member_to_remove.role == MemberRoleModel.OWNER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove project owner"
        )
    
    db.delete(member_to_remove)
    db.commit()
    
    return {"message": "Member removed successfully"}