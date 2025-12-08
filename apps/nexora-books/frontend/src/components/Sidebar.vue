<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h2>📚 Books</h2>
    </div>
    <nav class="sidebar-nav">
      <router-link to="/dashboard" class="nav-link">
        <span>📊</span> Dashboard
      </router-link>
      <router-link to="/books" class="nav-link">
        <span>📖</span> Books
      </router-link>
    </nav>
    <div class="sidebar-footer">
      <p>{{ userRole }}</p>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const userRole = ref('')

onMounted(() => {
  const user = localStorage.getItem('user')
  if (user) {
    const userData = JSON.parse(user)
    userRole.value = `Role: ${userData.role}`
  }
})
</script>

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
  flex: 1;
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

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 12px;
  text-align: center;
  color: #95a5a6;
}
</style>
