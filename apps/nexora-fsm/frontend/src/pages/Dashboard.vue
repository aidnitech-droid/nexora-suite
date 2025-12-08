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
