/* ════════════════════════════════════════
   api.js — Centralized API client + Toast
   ════════════════════════════════════════ */

const BASE_URL = 'http://127.0.0.1:8000';

const API = {
  // ── Auth ──────────────────────────────
  async signup(name, email, password, role) {
    return request('POST', '/auth/signup', { name, email, password, role });
  },
  async login(email, password) {
    return request('POST', '/auth/login', { email, password });
  },
  async me() {
    return request('GET', '/auth/me');
  },

  // ── Users ─────────────────────────────
  async getUsers() {
    return request('GET', '/users');
  },

  // ── Projects ──────────────────────────
  async getProjects() {
    return request('GET', '/projects');
  },
  async createProject(name, description) {
    return request('POST', '/projects', { name, description });
  },
  async deleteProject(id) {
    return request('DELETE', `/projects/${id}`);
  },
  async addMember(projectId, userId) {
    return request('POST', `/projects/${projectId}/members`, { user_id: userId });
  },
  async removeMember(projectId, userId) {
    return request('DELETE', `/projects/${projectId}/members/${userId}`);
  },

  // ── Tasks ──────────────────────────────
  async getMyTasks() {
    return request('GET', '/tasks');
  },
  async getProjectTasks(projectId) {
    return request('GET', `/projects/${projectId}/tasks`);
  },
  async createTask(projectId, payload) {
    return request('POST', `/projects/${projectId}/tasks`, payload);
  },
  async updateTask(taskId, payload) {
    return request('PATCH', `/tasks/${taskId}`, payload);
  },
  async deleteTask(taskId) {
    return request('DELETE', `/tasks/${taskId}`);
  },

  // ── Dashboard ─────────────────────────
  async getDashboard() {
    return request('GET', '/dashboard');
  },
};

async function request(method, path, body = null) {
  const token = localStorage.getItem('tm_token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(BASE_URL + path, opts);

  if (res.status === 401) {
    localStorage.removeItem('tm_token');
    localStorage.removeItem('tm_user');
    window.location.href = 'index.html';
    return;
  }

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const msg = data.detail
      ? (typeof data.detail === 'string' ? data.detail : data.detail.map(d => d.msg).join(', '))
      : `Error ${res.status}`;
    throw new Error(msg);
  }

  return data;
}

/* ── Toast utility (shared across pages) ── */
function showToast(msg, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const icons = { success: '✅', error: '❌', info: 'ℹ️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type]}</span><span>${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'fadeOut 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

/* ── Auth guard ── */
function requireAuth() {
  const token = localStorage.getItem('tm_token');
  if (!token) { window.location.href = 'index.html'; return null; }
  return JSON.parse(localStorage.getItem('tm_user') || 'null');
}

function logout() {
  localStorage.removeItem('tm_token');
  localStorage.removeItem('tm_user');
  window.location.href = 'index.html';
}

function getInitials(name) {
  if (!name) return '?';
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);
}

function formatDate(dt) {
  if (!dt) return '—';
  return new Date(dt).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

function isOverdue(deadline, status) {
  if (!deadline || status === 'completed') return false;
  return new Date(deadline) < new Date();
}
