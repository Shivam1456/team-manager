# 🚀 Team Manager — Full Stack App

A complete **Team Task Manager** with Role-Based Access Control, built with:
- **Backend**: Python + FastAPI + SQLite
- **Frontend**: HTML + CSS + Vanilla JS

https://team-manager-khaki.vercel.app/dashboard.html

<img width="1920" height="1080" alt="Screenshot (51)" src="https://github.com/user-attachments/assets/f90662d1-5b76-4a94-8451-22c5ecaa45e0" />
<img width="1920" height="1080" alt="Screenshot (59)" src="https://github.com/user-attachments/assets/81bae6ac-72a8-4da8-acd2-5342f97a7861" />
<img width="1920" height="1080" alt="Screenshot (58)" src="https://github.com/user-attachments/assets/fa843ba1-578f-4670-9bbc-ff8b79354760" />
<img width="1920" height="1080" alt="Screenshot (57)" src="https://github.com/user-attachments/assets/5b82d6d2-9e7f-4648-99a1-2186b4bb8497" />
<img width="1920" height="1080" alt="Screenshot (56)" src="https://github.com/user-attachments/assets/f795c3c1-2fa4-43a5-bd68-76d38ae04ba4" />
<img width="1920" height="1080" alt="Screenshot (55)" src="https://github.com/user-attachments/assets/9c37f9b9-32ce-4e19-b22f-20edc35f0cbd" />
<img width="1920" height="1080" alt="Screenshot (54)" src="https://github.com/user-attachments/assets/95cca907-35f8-4a5d-ac20-bb5b095f25ee" />
<img width="1920" height="1080" alt="Screenshot (53)" src="https://github.com/user-attachments/assets/953b8fe5-5f62-4780-88a0-6257c9403164" />
<img width="1920" height="1080" alt="Screenshot (52)" src="https://github.com/user-attachments/assets/82135c64-9b7b-4f5e-bf6f-f0c2142c1e4b" />
<img width="1920" height="1080" alt="Screenshot (50)" src="https://github.com/user-attachments/assets/e580b775-082d-425a-8c50-85b8e1c26fab" />
<img width="1920" height="1080" alt="Screenshot (49)" src="https://github.com/user-attachments/assets/c2b17abd-1c3b-4610-ab8f-7899248817bf" />












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
