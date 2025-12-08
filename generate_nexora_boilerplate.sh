#!/bin/bash

# Array of all app directories
APPS=(
  "nexora-payroll"
  "nexora-expense"
  "nexora-inventory"
  "nexora-billing"
  "nexora-invoice"
  "nexora-practice"
  "nexora-payments"
  "nexora-sign"
  "nexora-desk"
  "nexora-assist"
  "nexora-salesiq"
  "nexora-bookings"
  "nexora-fsm"
  "nexora-lens"
  "nexora-crm"
  "nexora-bigin"
  "nexora-forms"
  "nexora-route"
  "nexora-pos"
  "nexora-commerce"
  "nexora-checkout"
)

# Function to generate backend files
generate_backend() {
  local app_name=$1
  local app_dir="/workspaces/nexora-suite/apps/$app_name"
  
  echo "Generating backend for $app_name..."
  
  # Create requirements.txt
  cat > "$app_dir/requirements.txt" << 'EOF'
Flask==2.3.0
Flask-SQLAlchemy==3.0.5
Flask-JWT-Extended==4.4.4
python-dotenv==1.0.0
PyJWT==2.8.0
Werkzeug==2.3.0
SQLAlchemy==2.0.19
pytest==7.4.0
pytest-flask==1.2.0
gunicorn==21.2.0
EOF

  # Create Dockerfile
  cat > "$app_dir/Dockerfile" << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
EOF

  # Create .env file
  cat > "$app_dir/.env" << 'EOF'
DATABASE_URL=sqlite:///app.db
JWT_SECRET=your-secret-key-here
FLASK_ENV=development
EOF

  # Create app.py with generic module
  cat > "$app_dir/app.py" << EOF
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
import os
from datetime import timedelta

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'dev-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# ==================== Models ====================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, manager, user
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

class Module(db.Model):
    __tablename__ = 'module_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='active')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

# ==================== Role-based decorator ====================

def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or user.role not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# ==================== Auth Endpoints ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'user')
    )
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'access_token': access_token
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or user.password != data['password']:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'access_token': access_token
    }), 200

# ==================== CRUD Endpoints ====================

@app.route('/api/items', methods=['GET'])
def get_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    items = Module.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': items.total,
        'pages': items.pages,
        'current_page': page,
        'items': [{
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'status': item.status,
            'created_at': item.created_at
        } for item in items.items]
    }), 200

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Module.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    return jsonify({
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'status': item.status,
        'created_at': item.created_at
    }), 200

@app.route('/api/items', methods=['POST'])
@role_required(['admin', 'manager'])
def create_item():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    item = Module(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'active'),
        created_by=user_id
    )
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify({
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'status': item.status
    }), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
@role_required(['admin', 'manager'])
def update_item(item_id):
    item = Module.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    data = request.get_json()
    
    item.title = data.get('title', item.title)
    item.description = data.get('description', item.description)
    item.status = data.get('status', item.status)
    
    db.session.commit()
    
    return jsonify({
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'status': item.status
    }), 200

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_item(item_id):
    item = Module.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Item deleted successfully'}), 200

# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': '$app_name'}), 200

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
EOF

  # Create tests.py
  cat > "$app_dir/tests.py" << 'EOF'
import pytest
from app import app, db, User, Module

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_register(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201

def test_login(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
EOF
}

# Function to generate frontend files
generate_frontend() {
  local app_name=$1
  local app_dir="/workspaces/nexora-suite/apps/$app_name/frontend"
  local module_label="${app_name//-/ }"
  
  echo "Generating frontend for $app_name..."
  
  # Create directories
  mkdir -p "$app_dir/src/router"
  mkdir -p "$app_dir/src/services"
  mkdir -p "$app_dir/src/pages"
  mkdir -p "$app_dir/src/components"
  
  # Create package.json
  cat > "$app_dir/package.json" << EOF
{
  "name": "${app_name}-frontend",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.3.4",
    "vue-router": "^4.2.4",
    "axios": "^1.5.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.3.4",
    "vite": "^4.4.9"
  }
}
EOF

  # Create router/index.js
  cat > "$app_dir/src/router/index.js" << 'EOF'
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Dashboard from '../pages/Dashboard.vue'
import Items from '../pages/Items.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/items', name: 'Items', component: Items, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
EOF

  # Create services/api.js
  cat > "$app_dir/src/services/api.js" << 'EOF'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => Promise.reject(error))

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
EOF

  # Create services/itemService.js
  cat > "$app_dir/src/services/itemService.js" << 'EOF'
import api from './api'

export const authService = {
  login: (username, password) => api.post('/auth/login', { username, password }),
  register: (username, email, password) => api.post('/auth/register', { username, email, password })
}

export const itemService = {
  getItems: (page = 1, perPage = 10) => api.get('/items', { params: { page, per_page: perPage } }),
  getItem: (id) => api.get(`/items/${id}`),
  createItem: (data) => api.post('/items', data),
  updateItem: (id, data) => api.put(`/items/${id}`, data),
  deleteItem: (id) => api.delete(`/items/${id}`)
}
EOF

  # Create pages/Login.vue
  cat > "$app_dir/src/pages/Login.vue" << 'EOF'
<template>
  <div class="login-container">
    <div class="login-form">
      <h1>Module Management</h1>
      <form @submit.prevent="handleLogin">
        <input v-model="form.username" type="text" placeholder="Username" required />
        <input v-model="form.password" type="password" placeholder="Password" required />
        <button type="submit" class="btn-login">Login</button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/itemService'

const form = ref({ username: '', password: '' })
const error = ref('')
const router = useRouter()

const handleLogin = async () => {
  try {
    const response = await authService.login(form.value.username, form.value.password)
    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('user', JSON.stringify(response.data))
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.error || 'Login failed'
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-form {
  background: white;
  padding: 40px;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.btn-login {
  width: 100%;
  padding: 10px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.error {
  color: #e74c3c;
  margin-top: 15px;
}
</style>
EOF

  # Create pages/Dashboard.vue
  cat > "$app_dir/src/pages/Dashboard.vue" << 'EOF'
<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="dashboard-header">
        <h1>Dashboard</h1>
        <button @click="logout" class="btn-logout">Logout</button>
      </div>
      <div class="stats-grid">
        <div class="stat-card">
          <h3>Total Items</h3>
          <p class="stat-number">{{ stats.totalItems }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import { itemService } from '../services/itemService'

const router = useRouter()
const stats = ref({ totalItems: 0 })

onMounted(async () => {
  try {
    const response = await itemService.getItems(1, 1000)
    stats.value.totalItems = response.data.items.length
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
})

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
  background: #f5f5f5;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.btn-logout {
  padding: 8px 16px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #667eea;
}
</style>
EOF

  # Create pages/Items.vue
  cat > "$app_dir/src/pages/Items.vue" << 'EOF'
<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="header">
        <h1>Items Management</h1>
        <button @click="showCreateForm = true" class="btn-add">+ Add Item</button>
      </div>

      <div v-if="showCreateForm" class="modal">
        <div class="modal-content">
          <h2>Add New Item</h2>
          <form @submit.prevent="handleCreateItem">
            <input v-model="newItem.title" placeholder="Title" required />
            <textarea v-model="newItem.description" placeholder="Description"></textarea>
            <div class="form-actions">
              <button type="submit" class="btn-save">Save</button>
              <button type="button" @click="showCreateForm = false" class="btn-cancel">Cancel</button>
            </div>
          </form>
        </div>
      </div>

      <div class="items-list">
        <div v-for="item in items" :key="item.id" class="item-card">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <button @click="handleDeleteItem(item.id)" class="btn-delete">Delete</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { itemService } from '../services/itemService'

const items = ref([])
const showCreateForm = ref(false)
const newItem = ref({ title: '', description: '' })

onMounted(loadItems)

async function loadItems() {
  try {
    const response = await itemService.getItems()
    items.value = response.data.items
  } catch (error) {
    console.error('Failed to load items:', error)
  }
}

async function handleCreateItem() {
  try {
    await itemService.createItem(newItem.value)
    showCreateForm.value = false
    newItem.value = { title: '', description: '' }
    await loadItems()
  } catch (error) {
    console.error('Failed to create item:', error)
  }
}

async function handleDeleteItem(id) {
  if (confirm('Delete this item?')) {
    try {
      await itemService.deleteItem(id)
      await loadItems()
    } catch (error) {
      console.error('Failed to delete item:', error)
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
  background: #f5f5f5;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.btn-add {
  padding: 10px 20px;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
}

input, textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.form-actions {
  display: flex;
  gap: 10px;
}

.btn-save, .btn-cancel {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-save {
  background: #667eea;
  color: white;
}

.btn-cancel {
  background: #ddd;
}

.items-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.item-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.item-card h3 {
  margin-top: 0;
}

.btn-delete {
  width: 100%;
  padding: 8px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}
</style>
EOF

  # Create components/Sidebar.vue
  cat > "$app_dir/src/components/Sidebar.vue" << 'EOF'
<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h2>📋 Module</h2>
    </div>
    <nav class="sidebar-nav">
      <router-link to="/dashboard" class="nav-link">
        <span>📊</span> Dashboard
      </router-link>
      <router-link to="/items" class="nav-link">
        <span>📝</span> Items
      </router-link>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 250px;
  background: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  height: 100vh;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 20px;
}

.sidebar-nav {
  padding: 20px 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  color: white;
  text-decoration: none;
  transition: background 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background: #34495e;
}

.nav-link span {
  margin-right: 10px;
  font-size: 18px;
}
</style>
EOF

  # Create main.js
  cat > "$app_dir/src/main.js" << 'EOF'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)
app.mount('#app')
EOF

  # Create App.vue
  cat > "$app_dir/src/App.vue" << 'EOF'
<template>
  <router-view />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f5;
}
</style>
EOF

  # Create vite.config.js
  cat > "$app_dir/vite.config.js" << 'EOF'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
EOF

  # Create index.html
  cat > "$app_dir/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Module Management</title>
</head>
<body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
</body>
</html>
EOF

  # Create .gitignore
  cat > "$app_dir/.gitignore" << 'EOF'
.env.local
node_modules
dist
EOF
}

# Generate boilerplate for all apps (except nexora-books which is already done)
for app in "${APPS[@]}"; do
  generate_backend "$app"
  generate_frontend "$app"
done

echo "✅ Boilerplate generation complete!"
