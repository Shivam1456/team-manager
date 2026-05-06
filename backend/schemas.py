from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    member = "member"


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


# ─── Auth ───────────────────────────────────────────────────────
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.member

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ─── User ───────────────────────────────────────────────────────
class UserBrief(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str
    email: str
    role: UserRole


class UserOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str
    email: str
    role: UserRole
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ─── Project ────────────────────────────────────────────────────
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Project name cannot be empty")
        return v.strip()


class TaskBrief(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    title: str
    status: TaskStatus
    deadline: Optional[datetime] = None
    assignee_id: int


class ProjectOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    created_at: datetime
    members: List[UserBrief] = []
    tasks: List[TaskBrief] = []


class AddMemberRequest(BaseModel):
    user_id: int


# ─── Task ───────────────────────────────────────────────────────
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assignee_id: int
    deadline: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Task title cannot be empty")
        return v.strip()


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None
    deadline: Optional[datetime] = None


class ProjectBrief(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str


class TaskOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    deadline: Optional[datetime] = None
    project_id: int
    assignee_id: int
    created_at: datetime
    assignee: UserBrief
    project: ProjectBrief


# ─── Dashboard ──────────────────────────────────────────────────
class DashboardStats(BaseModel):
    total_tasks: int
    pending: int
    in_progress: int
    completed: int
    overdue: int
    projects_count: int
