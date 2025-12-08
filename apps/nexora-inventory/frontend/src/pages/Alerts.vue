<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>🚨 Stock Alerts</h1>
      </div>

      <div class="filters">
        <select v-model="filters.status" class="filter-select" @change="loadAlerts()">
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="resolved">Resolved</option>
        </select>
        
        <select v-model="filters.type" class="filter-select" @change="loadAlerts()">
          <option value="">All Types</option>
          <option value="low_stock">Low Stock</option>
          <option value="expired">Expired</option>
          <option value="overstock">Overstock</option>
        </select>
      </div>

      <div v-if="loading" class="loading">Loading alerts...</div>

      <div v-else class="alerts-container">
        <div v-if="alerts.length === 0" class="no-alerts">
          <p>No alerts found</p>
        </div>

        <div v-for="alert in alerts" :key="alert.id" class="alert-card" :class="alert.alert_type">
          <div class="alert-header">
            <span class="alert-icon">
              <span v-if="alert.alert_type === 'low_stock'">⚠️</span>
              <span v-else-if="alert.alert_type === 'expired'">⛔</span>
              <span v-else>📦</span>
            </span>
            <div class="alert-title">
              <h3>{{ alert.item_name }}</h3>
              <p class="alert-type">{{ formatAlertType(alert.alert_type) }}</p>
            </div>
            <span class="status-badge" :class="alert.is_resolved ? 'resolved' : 'active'">
              {{ alert.is_resolved ? 'Resolved' : 'Active' }}
            </span>
          </div>

          <div class="alert-body">
            <p class="alert-message">{{ alert.message }}</p>
            
            <div class="alert-details">
              <div class="detail-item">
                <span class="detail-label">Current Stock:</span>
                <span class="detail-value">{{ alert.current_stock }} units</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Threshold:</span>
                <span class="detail-value">{{ alert.threshold }} units</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Created:</span>
                <span class="detail-value">{{ formatDate(alert.created_at) }}</span>
              </div>
            </div>
          </div>

          <div class="alert-actions">
            <button 
              v-if="!alert.is_resolved"
              @click="resolveAlert(alert.id)"
              class="btn-resolve"
            >
              Mark as Resolved
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { inventoryService } from '../services/inventoryService'

const loading = ref(false)
const alerts = ref([])

const filters = ref({
  status: 'active',
  type: ''
})

const loadAlerts = async () => {
  try {
    loading.value = true
    const params = {
      is_resolved: filters.value.status === 'resolved' ? true : filters.value.status === 'active' ? false : undefined,
      alert_type: filters.value.type || undefined
    }
    const response = await inventoryService.getAlerts(1, 100, params)
    alerts.value = response.data.alerts
  } catch (error) {
    console.error('Failed to load alerts:', error)
  } finally {
    loading.value = false
  }
}

const formatAlertType = (type) => {
  const types = {
    low_stock: 'Low Stock',
    expired: 'Expired Stock',
    overstock: 'Overstock'
  }
  return types[type] || type
}

const formatDate = (date) => new Date(date).toLocaleDateString()

const resolveAlert = async (id) => {
  try {
    await inventoryService.resolveAlert(id)
    alert('Alert marked as resolved')
    await loadAlerts()
  } catch (error) {
    console.error('Failed to resolve alert:', error)
    alert('Failed to resolve alert')
  }
}

onMounted(() => {
  loadAlerts()
})
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

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.alerts-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 20px;
}

.alert-card {
  background: white;
  border-radius: 8px;
  border-left: 5px solid #f39c12;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.alert-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.alert-card.low_stock {
  border-left-color: #f39c12;
  background: linear-gradient(135deg, rgba(243, 156, 18, 0.05) 0%, transparent 100%);
}

.alert-card.expired {
  border-left-color: #e74c3c;
  background: linear-gradient(135deg, rgba(231, 76, 60, 0.05) 0%, transparent 100%);
}

.alert-card.overstock {
  border-left-color: #3498db;
  background: linear-gradient(135deg, rgba(52, 152, 219, 0.05) 0%, transparent 100%);
}

.alert-header {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.alert-icon {
  font-size: 24px;
}

.alert-title {
  flex: 1;
}

.alert-title h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.alert-type {
  margin: 4px 0 0 0;
  font-size: 12px;
  color: #999;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.active {
  background: #ffe6e6;
  color: #e74c3c;
}

.status-badge.resolved {
  background: #d4edda;
  color: #27ae60;
}

.alert-body {
  padding: 15px;
}

.alert-message {
  margin: 0 0 15px 0;
  color: #555;
  line-height: 1.5;
}

.alert-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 12px;
  color: #999;
  font-weight: 600;
}

.detail-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.alert-actions {
  padding: 12px 15px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 8px;
}

.btn-resolve {
  flex: 1;
  padding: 8px 12px;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  font-size: 12px;
}

.btn-resolve:hover {
  background: #229954;
}

.no-alerts {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 8px;
  color: #999;
}

.loading {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 8px;
}
</style>
