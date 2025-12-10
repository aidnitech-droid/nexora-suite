#!/bin/bash

# Nexora Suite - Module Frontend Template Generator
# This script creates a complete Vue.js frontend for any Nexora module

MODULE_NAME=$1
MODULE_PATH="./apps/${MODULE_NAME}"

if [ -z "$MODULE_NAME" ]; then
    echo "Usage: ./generate_module_frontend.sh <module-name>"
    echo "Example: ./generate_module_frontend.sh nexora-payments"
    exit 1
fi

if [ ! -d "$MODULE_PATH" ]; then
    echo "Error: Module directory $MODULE_PATH not found"
    exit 1
fi

echo "🔧 Generating frontend for $MODULE_NAME..."

# Create directory structure
mkdir -p "$MODULE_PATH/frontend/src/pages"
mkdir -p "$MODULE_PATH/frontend/src/components"
mkdir -p "$MODULE_PATH/frontend/src/services"
mkdir -p "$MODULE_PATH/frontend/src/router"
mkdir -p "$MODULE_PATH/frontend/public"

echo "✅ Created directory structure"

# Create package.json
cat > "$MODULE_PATH/frontend/package.json" << 'EOF'
{
  "name": "MODULE_FRONTEND",
  "version": "1.0.0",
  "description": "Nexora Module Frontend",
  "main": "index.js",
  "scripts": {
    "serve": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "dev": "vue-cli-service serve",
    "test": "jest"
  },
  "dependencies": {
    "vue": "^2.6.14",
    "vue-router": "^3.6.5",
    "axios": "^1.4.0"
  },
  "devDependencies": {
    "@vue/cli-service": "^5.0.0",
    "vue-template-compiler": "^2.6.14"
  }
}
EOF

sed -i "s/MODULE_FRONTEND/${MODULE_NAME}-frontend/g" "$MODULE_PATH/frontend/package.json"
echo "✅ Created package.json"

# Create index.html
cat > "$MODULE_PATH/frontend/public/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexora Module</title>
</head>
<body>
    <div id="app"></div>
    <script src="/js/app.js"></script>
</body>
</html>
EOF

MODULE_DISPLAY=$(echo "$MODULE_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))} 1')
sed -i "s/Nexora Module/Nexora ${MODULE_DISPLAY}/g" "$MODULE_PATH/frontend/public/index.html"
echo "✅ Created index.html"

# Create service file
cat > "$MODULE_PATH/frontend/src/services/api.js" << 'EOF'
import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000/api';

export default {
  // Generic CRUD operations
  list(resource, page = 1, perPage = 10, filters = {}) {
    return axios.get(`${API_URL}/${resource}`, { params: { page, per_page: perPage, ...filters } });
  },

  get(resource, id) {
    return axios.get(`${API_URL}/${resource}/${id}`);
  },

  create(resource, data) {
    return axios.post(`${API_URL}/${resource}`, data);
  },

  update(resource, id, data) {
    return axios.put(`${API_URL}/${resource}/${id}`, data);
  },

  delete(resource, id) {
    return axios.delete(`${API_URL}/${resource}/${id}`);
  },

  // Health check
  health() {
    return axios.get(`${API_URL}/health`);
  }
};
EOF

echo "✅ Created API service"

# Create router
cat > "$MODULE_PATH/frontend/src/router/index.js" << 'EOF'
import Vue from 'vue';
import VueRouter from 'vue-router';
import Dashboard from '../pages/Dashboard.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'Dashboard' }
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Nexora';
  next();
});

export default router;
EOF

echo "✅ Created router"

# Create main.js
cat > "$MODULE_PATH/frontend/src/main.js" << 'EOF'
import Vue from 'vue';
import App from './App.vue';
import router from './router';

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App)
}).$mount('#app');
EOF

echo "✅ Created main.js"

# Create Dashboard component
cat > "$MODULE_PATH/frontend/src/pages/Dashboard.vue" << 'EOF'
<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Nexora Module Dashboard</h1>
      <p>Welcome to your module</p>
    </div>

    <div class="welcome-section">
      <div class="welcome-card">
        <h2>Getting Started</h2>
        <p>This is your module dashboard. Start by exploring the features available.</p>
        <ul>
          <li>📊 View your data and statistics</li>
          <li>➕ Create and manage items</li>
          <li>⚙️ Configure settings</li>
          <li>📈 Track performance</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard'
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.dashboard-header {
  margin-bottom: 30px;
}

.dashboard-header h1 {
  font-size: 28px;
  color: #333;
  margin: 0 0 5px 0;
}

.dashboard-header p {
  color: #666;
  margin: 0;
}

.welcome-section {
  margin-bottom: 30px;
}

.welcome-card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.welcome-card h2 {
  margin: 0 0 15px 0;
  color: #333;
}

.welcome-card p {
  color: #666;
  margin-bottom: 15px;
  line-height: 1.6;
}

.welcome-card ul {
  margin: 0;
  padding-left: 20px;
}

.welcome-card li {
  margin: 8px 0;
  color: #666;
}
</style>
EOF

echo "✅ Created Dashboard component"

# Create App.vue
cat > "$MODULE_PATH/frontend/src/App.vue" << 'EOF'
<template>
  <div id="app">
    <nav class="navbar">
      <div class="navbar-brand">
        <router-link to="/" class="brand">
          <span class="logo">📦</span>
          <span>Nexora</span>
        </router-link>
      </div>
      <ul class="navbar-menu">
        <li><router-link to="/">Dashboard</router-link></li>
      </ul>
    </nav>

    <main class="main-content">
      <router-view></router-view>
    </main>

    <footer class="footer">
      <p>&copy; 2025 Nexora Suite. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
    'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans',
    'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.navbar {
  background: white;
  padding: 15px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand {
  color: #007bff;
  text-decoration: none;
  font-size: 20px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo {
  font-size: 24px;
}

.navbar-menu {
  display: flex;
  list-style: none;
  gap: 30px;
}

.navbar-menu a {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.navbar-menu a:hover,
.navbar-menu a.router-link-active {
  color: #007bff;
}

.main-content {
  flex: 1;
  padding: 0;
}

.footer {
  background: white;
  padding: 20px;
  text-align: center;
  color: #999;
  border-top: 1px solid #ddd;
  margin-top: 40px;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .navbar-menu {
    flex-direction: column;
    gap: 10px;
    width: 100%;
  }
}
</style>
EOF

echo "✅ Created App.vue"

echo ""
echo "✨ Frontend generation complete for $MODULE_NAME!"
echo ""
echo "Next steps:"
echo "1. cd $MODULE_PATH/frontend"
echo "2. npm install"
echo "3. npm run dev"
echo ""
