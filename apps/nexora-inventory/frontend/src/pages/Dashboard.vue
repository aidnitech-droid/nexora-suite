<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="dashboard-header">
        <h1>📊 Inventory Dashboard</h1>
        <button @click="refreshData" class="btn-refresh">Refresh</button>
      </div>

      <div v-if="loading" class="loading">Loading analytics...</div>

      <div v-else class="analytics-grid">
        <!-- Summary Cards -->
        <div class="stat-card">
          <div class="stat-icon">📦</div>
          <h3>Total Items</h3>
          <p class="stat-value">{{ analytics.total_items }}</p>
        </div>

        <div class="stat-card">
          <div class="stat-icon">🏭</div>
          <h3>Warehouses</h3>
          <p class="stat-value">{{ analytics.total_warehouses }}</p>
        </div>

        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <h3>Stock Value</h3>
          <p class="stat-value">${{ formatCurrency(analytics.total_stock_value) }}</p>
        </div>

        <div class="stat-card warning">
          <div class="stat-icon">⚠️</div>
          <h3>Low Stock Items</h3>
          <p class="stat-value">{{ analytics.low_stock_items }}</p>
        </div>

        <div class="stat-card">
          <div class="stat-icon">🔔</div>
          <h3>Active Alerts</h3>
          <p class="stat-value">{{ analytics.active_alerts }}</p>
        </div>

        <div class="stat-card">
          <div class="stat-icon">📥</div>
          <h3>Pending POs</h3>
          <p class="stat-value">{{ analytics.pending_purchase_orders }}</p>
        </div>

        <div class="stat-card">
          <div class="stat-icon">📤</div>
          <h3>Pending SOs</h3>
          <p class="stat-value">{{ analytics.pending_sale_orders }}</p>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="charts-section" v-if="!loading">
        <div class="chart-container">
          <h2>Stock Value by Category</h2>
          <div class="category-breakdown">
            <div v-for="cat in categoryData" :key="cat.category" class="category-item">
              <span class="category-name">{{ cat.category }}</span>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: cat.percentage + '%' }"></div>
              </div>
              <span class="category-value">${{ formatCurrency(cat.total_value) }}</span>
            </div>
          </div>
        </div>

        <div class="chart-container">
          <h2>Warehouse Utilization</h2>
          <div class="warehouse-stats">
            <div v-for="wh in warehouseData" :key="wh.warehouse_id" class="warehouse-item">
              <span class="warehouse-name">{{ wh.warehouse_name }}</span>
              <div class="progress-bar">
                <div 
                  class="progress-fill"
                  :style="{ 
                    width: wh.utilization_percent + '%',
                    backgroundColor: wh.utilization_percent > 80 ? '#e74c3c' : '#27ae60'
                  }"
                ></div>
              </div>
              <span class="warehouse-value">{{ wh.current_usage }}/{{ wh.capacity }} ({{ wh.utilization_percent }}%)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Links -->
      <div class="quick-actions">
        <router-link to="/inventory" class="action-button">
            <span>📋</span> Manage Items
          </router-link>
        <router-link to="/warehouses" class="action-button">
          <span>🏭</span> Warehouses
        </router-link>
        <router-link to="/purchase-orders" class="action-button">
          <span>📥</span> Purchase Orders
        </router-link>
        <router-link to="/sale-orders" class="action-button">
          <span>📤</span> Sale Orders
        </router-link>
        <router-link to="/alerts" class="action-button">
          <span>🔔</span> Stock Alerts
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { inventoryService } from '../services/inventoryService'

const loading = ref(false)
const analytics = ref({
  total_items: 0,
  total_warehouses: 0,
  total_stock_value: 0,
  low_stock_items: 0,
  pending_purchase_orders: 0,
  pending_sale_orders: 0,
  active_alerts: 0
})

const categoryData = ref([])
const warehouseData = ref([])

const loadAnalytics = async () => {
  try {
    loading.value = true
    
    const [summary, stockValue, warehouseCap] = await Promise.all([
      inventoryService.getAnalyticsSummary(),
      inventoryService.getStockValueByCategory(),
      inventoryService.getWarehouseCapacity()
    ])
    
    analytics.value = summary.data
    
    // Process category data
    const maxValue = Math.max(...stockValue.data.map(d => d.total_value), 1)
    categoryData.value = stockValue.data.map(cat => ({
      ...cat,
      percentage: (cat.total_value / maxValue * 100).toFixed(1)
    }))
    
    warehouseData.value = warehouseCap.data
  } catch (error) {
    console.error('Failed to load analytics:', error)
  } finally {
    loading.value = false
  }
}

const formatCurrency = (value) => {
  return parseFloat(value).toFixed(2)
}

const refreshData = () => {
  loadAnalytics()
}

onMounted(() => {
  loadAnalytics()
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

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.dashboard-header h1 {
  margin: 0;
  font-size: 28px;
}

.btn-refresh {
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-refresh:hover {
  background: #2980b9;
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card.warning {
  border-left: 4px solid #f39c12;
}

.stat-icon {
  font-size: 32px;
  margin-bottom: 10px;
}

.stat-card h3 {
  margin: 10px 0;
  color: #333;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  color: #27ae60;
}

.loading {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 8px;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.chart-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart-container h2 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
}

.category-breakdown,
.warehouse-stats {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.category-item,
.warehouse-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-name,
.warehouse-name {
  flex: 0 0 120px;
  font-weight: 500;
  color: #333;
}

.progress-bar {
  flex: 1;
  height: 25px;
  background: #ecf0f1;
  border-radius: 12px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #3498db;
  transition: width 0.3s;
}

.category-value,
.warehouse-value {
  flex: 0 0 150px;
  text-align: right;
  font-weight: 600;
  color: #27ae60;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.action-button {
  padding: 20px;
  background: white;
  border: 2px solid #3498db;
  border-radius: 8px;
  text-decoration: none;
  color: #333;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.action-button span {
  font-size: 28px;
}

.action-button:hover {
  background: #3498db;
  color: white;
}
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
