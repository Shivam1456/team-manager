from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import models, schemas, auth
from database import engine, get_db

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Team Manager API", version="1.0.0")

# ─── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ══════════════════════════════════════════════════════════════
#  AUTH ROUTES
# ══════════════════════════════════════════════════════════════
@app.post("/auth/signup", response_model=schemas.TokenResponse, status_code=201)
def signup(payload: schemas.SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        name=payload.name,
        email=payload.email,
        hashed_password=auth.hash_password(payload.password),
        role=models.UserRole(payload.role.value),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user}


@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not auth.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user}


@app.get("/auth/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


# ══════════════════════════════════════════════════════════════
#  USERS
# ══════════════════════════════════════════════════════════════
@app.get("/users", response_model=List[schemas.UserBrief])
def list_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.User).filter(models.User.is_active == True).all()


# ══════════════════════════════════════════════════════════════
#  PROJECTS
# ══════════════════════════════════════════════════════════════
@app.post("/projects", response_model=schemas.ProjectOut, status_code=201)
def create_project(
    payload: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    project = models.Project(
        name=payload.name,
        description=payload.description,
        owner_id=current_user.id,
    )
    project.members.append(current_user)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@app.get("/projects", response_model=List[schemas.ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role == models.UserRole.admin:
        return db.query(models.Project).all()
    return current_user.projects


@app.get("/projects/{project_id}", response_model=schemas.ProjectOut)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.role != models.UserRole.admin and current_user not in project.members:
        raise HTTPException(status_code=403, detail="Access denied")
    return project


@app.delete("/projects/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()


@app.post("/projects/{project_id}/members", response_model=schemas.ProjectOut)
def add_member(
    project_id: int,
    payload: schemas.AddMemberRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user not in project.members:
        project.members.append(user)
        db.commit()
        db.refresh(project)
    return project


@app.delete("/projects/{project_id}/members/{user_id}", response_model=schemas.ProjectOut)
def remove_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user and user in project.members:
        project.members.remove(user)
        db.commit()
        db.refresh(project)
    return project


# ══════════════════════════════════════════════════════════════
#  TASKS
# ══════════════════════════════════════════════════════════════
@app.post("/projects/{project_id}/tasks", response_model=schemas.TaskOut, status_code=201)
def create_task(
    project_id: int,
    payload: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    assignee = db.query(models.User).filter(models.User.id == payload.assignee_id).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee not found")

    task = models.Task(
        title=payload.title,
        description=payload.description,
        assignee_id=payload.assignee_id,
        deadline=payload.deadline,
        project_id=project_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.get("/projects/{project_id}/tasks", response_model=List[schemas.TaskOut])
def list_project_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.role != models.UserRole.admin and current_user not in project.members:
        raise HTTPException(status_code=403, detail="Access denied")

    tasks = db.query(models.Task).filter(models.Task.project_id == project_id)
    if current_user.role == models.UserRole.member:
        tasks = tasks.filter(models.Task.assignee_id == current_user.id)
    return tasks.all()


@app.get("/tasks", response_model=List[schemas.TaskOut])
def list_my_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """All tasks for the current user (member sees own; admin sees all)"""
    if current_user.role == models.UserRole.admin:
        return db.query(models.Task).all()
    return db.query(models.Task).filter(models.Task.assignee_id == current_user.id).all()


@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role == models.UserRole.member and task.assignee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return task


@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    payload: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Members can only update status of their own tasks
    if current_user.role == models.UserRole.member:
        if task.assignee_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        if payload.status:
            task.status = models.TaskStatus(payload.status.value)
    else:
        # Admin can update everything
        if payload.title is not None:
            task.title = payload.title
        if payload.description is not None:
            task.description = payload.description
        if payload.status is not None:
            task.status = models.TaskStatus(payload.status.value)
        if payload.assignee_id is not None:
            task.assignee_id = payload.assignee_id
        if payload.deadline is not None:
            task.deadline = payload.deadline

    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()


# ══════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════
@app.get("/dashboard", response_model=schemas.DashboardStats)
def dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    now = datetime.utcnow()

    if current_user.role == models.UserRole.admin:
        tasks = db.query(models.Task).all()
        projects_count = db.query(models.Project).count()
    else:
        tasks = db.query(models.Task).filter(models.Task.assignee_id == current_user.id).all()
        projects_count = len(current_user.projects)

    total = len(tasks)
    pending = sum(1 for t in tasks if t.status == models.TaskStatus.pending)
    in_progress = sum(1 for t in tasks if t.status == models.TaskStatus.in_progress)
    completed = sum(1 for t in tasks if t.status == models.TaskStatus.completed)
    overdue = sum(
        1 for t in tasks
        if t.deadline and t.deadline < now and t.status != models.TaskStatus.completed
    )

    return {
        "total_tasks": total,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
        "overdue": overdue,
        "projects_count": projects_count,
    }


@app.get("/")
def root():
    return {"message": "Team Manager API is running!", "docs": "/docs"}
