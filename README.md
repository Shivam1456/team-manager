# 🚀 Team Manager — Full Stack App

A complete **Team Task Manager** with Role-Based Access Control, built with:
- **Backend**: Python + FastAPI + SQLite
- **Frontend**: HTML + CSS + Vanilla JS

---

## 📂 Project Structure

```
Team Manager Task/
├── backend/
│   ├── main.py          # FastAPI app + all REST endpoints
│   ├── models.py        # SQLAlchemy DB models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── auth.py          # JWT auth + RBAC
│   ├── database.py      # DB connection
│   └── requirements.txt
│
└── frontend/
    ├── index.html       # Login / Signup
    ├── dashboard.html   # Overview dashboard
    ├── projects.html    # Project management
    ├── tasks.html       # Task management
    ├── admin.html       # Admin-only panel
    ├── api.js           # Centralized API client
    └── style.css        # Full design system
```

---

## ⚙️ Setup & Run

### 1. Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload --port 8000
```

Backend runs at: **http://127.0.0.1:8000**  
API Docs: **http://127.0.0.1:8000/docs**

### 2. Frontend

Open **`frontend/index.html`** directly in your browser  
*(No build step needed — pure HTML/CSS/JS)*

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Create account |
| POST | `/auth/login` | Login |
| GET | `/auth/me` | Current user |
| GET | `/users` | All users (auth required) |
| POST | `/projects` | Create project (Admin) |
| GET | `/projects` | List projects |
| POST | `/projects/{id}/members` | Add member (Admin) |
| DELETE | `/projects/{id}/members/{uid}` | Remove member (Admin) |
| POST | `/projects/{id}/tasks` | Create task (Admin) |
| GET | `/tasks` | My tasks |
| PATCH | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task (Admin) |
| GET | `/dashboard` | Dashboard stats |

---

## 👥 Roles

| Feature | Admin | Member |
|---------|-------|--------|
| Create project | ✅ | ❌ |
| Add/remove members | ✅ | ❌ |
| Create tasks | ✅ | ❌ |
| Delete tasks/projects | ✅ | ❌ |
| View all tasks | ✅ | ❌ (own only) |
| Update task status | ✅ | ✅ (own only) |

---

## 🧪 Quick Test Flow

1. **Signup** as Admin → `admin@test.com` / `password123`
2. **Create a project** from Projects page
3. **Signup** as Member → `member@test.com` / `password123`
4. Admin adds member to project
5. Admin creates a task and assigns to member
6. Member logs in → sees their task → updates status
7. Dashboard shows real-time stats!
