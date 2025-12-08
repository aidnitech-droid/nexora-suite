<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>🏢 Warehouses</h1>
        <button @click="showCreateForm = true" class="btn-primary">+ New Warehouse</button>
      </div>

      <div v-if="loading" class="loading">Loading warehouses...</div>

      <div v-else class="warehouses-grid">
        <div v-for="warehouse in warehouses" :key="warehouse.id" class="warehouse-card">
          <div class="warehouse-header">
            <h3>{{ warehouse.name }}</h3>
            <span class="status-badge" :class="warehouse.is_active ? 'active' : 'inactive'">
              {{ warehouse.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>

          <div class="warehouse-info">
            <div class="info-item">
              <span class="label">Location</span>
              <span class="value">📍 {{ warehouse.location }}</span>
            </div>
            
            <div class="info-item">
              <span class="label">Manager</span>
              <span class="value">👤 {{ warehouse.manager_name || 'Unassigned' }}</span>
            </div>

            <div class="capacity-info">
              <span class="label">Capacity</span>
              <div class="capacity-bar">
                <div class="capacity-used" :style="{ width: getCapacityPercent(warehouse) + '%' }"></div>
              </div>
              <span class="capacity-text">
                {{ warehouse.current_items || 0 }} / {{ warehouse.capacity }} items
              </span>
            </div>
          </div>

          <div class="warehouse-stats">
            <div class="stat">
              <span class="stat-value">{{ warehouse.total_stock_value }}</span>
              <span class="stat-label">Stock Value</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ warehouse.items_count || 0 }}</span>
              <span class="stat-label">Item Types</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ warehouse.total_units || 0 }}</span>
              <span class="stat-label">Total Units</span>
            </div>
          </div>

          <div class="warehouse-actions">
            <button @click="viewWarehouse(warehouse.id)" class="btn-view">View Details</button>
            <button @click="editWarehouse(warehouse.id)" class="btn-edit">Edit</button>
          </div>
        </div>
      </div>

      <!-- Create/Edit Warehouse Modal -->
      <div v-if="showCreateForm" class="modal-overlay" @click="showCreateForm = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ editingId ? 'Edit Warehouse' : 'Create Warehouse' }}</h2>
            <button @click="showCreateForm = false" class="btn-close">×</button>
          </div>
          
          <form @submit.prevent="saveWarehouse" class="form">
            <div class="form-group">
              <label>Warehouse Name</label>
              <input v-model="warehouseForm.name" required />
            </div>
            
            <div class="form-group">
              <label>Location</label>
              <input v-model="warehouseForm.location" required />
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label>Capacity (items)</label>
                <input v-model.number="warehouseForm.capacity" type="number" required />
              </div>
              
              <div class="form-group">
                <label>Manager ID</label>
                <input v-model.number="warehouseForm.manager_id" type="number" />
              </div>
            </div>
            
            <div class="form-group">
              <label>
                <input v-model="warehouseForm.is_active" type="checkbox" />
                Active
              </label>
            </div>
            
            <div class="form-actions">
              <button type="submit" class="btn-primary">{{ editingId ? 'Update' : 'Create' }}</button>
              <button type="button" @click="showCreateForm = false" class="btn-secondary">Cancel</button>
            </div>
          </form>
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
const showCreateForm = ref(false)
const editingId = ref(null)
const warehouses = ref([])

const warehouseForm = ref({
  name: '',
  location: '',
  capacity: 0,
  manager_id: null,
  is_active: true
})

const loadWarehouses = async () => {
  try {
    loading.value = true
    const response = await inventoryService.getWarehouses()
    warehouses.value = response.data
  } catch (error) {
    console.error('Failed to load warehouses:', error)
  } finally {
    loading.value = false
  }
}

const getCapacityPercent = (warehouse) => {
  if (!warehouse.capacity || warehouse.capacity === 0) return 0
  return Math.round(((warehouse.current_items || 0) / warehouse.capacity) * 100)
}

const resetForm = () => {
  warehouseForm.value = {
    name: '',
    location: '',
    capacity: 0,
    manager_id: null,
    is_active: true
  }
  editingId.value = null
}

const saveWarehouse = async () => {
  try {
    if (editingId.value) {
      await inventoryService.updateWarehouse(editingId.value, warehouseForm.value)
      alert('Warehouse updated')
    } else {
      await inventoryService.createWarehouse(warehouseForm.value)
      alert('Warehouse created')
    }
    showCreateForm.value = false
    resetForm()
    await loadWarehouses()
  } catch (error) {
    console.error('Failed to save warehouse:', error)
    alert('Failed to save warehouse')
  }
}

const viewWarehouse = (id) => {
  alert(`Warehouse ${id} details would open here`)
}

const editWarehouse = async (id) => {
  const warehouse = warehouses.value.find(w => w.id === id)
  if (warehouse) {
    warehouseForm.value = {
      name: warehouse.name,
      location: warehouse.location,
      capacity: warehouse.capacity,
      manager_id: warehouse.manager_id,
      is_active: warehouse.is_active
    }
    editingId.value = id
    showCreateForm.value = true
  }
}

onMounted(() => {
  loadWarehouses()
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0;
}

.btn-primary {
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.btn-primary:hover {
  background: #2980b9;
}

.warehouses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.warehouse-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.warehouse-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.warehouse-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.warehouse-header h3 {
  margin: 0;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.active {
  background: rgba(255, 255, 255, 0.3);
  color: white;
}

.status-badge.inactive {
  background: rgba(0, 0, 0, 0.2);
  color: white;
}

.warehouse-info {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
}

.label {
  font-size: 12px;
  color: #999;
  font-weight: 600;
  text-transform: uppercase;
}

.value {
  font-size: 14px;
  color: #333;
}

.capacity-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.capacity-bar {
  width: 100%;
  height: 8px;
  background: #eee;
  border-radius: 4px;
  overflow: hidden;
}

.capacity-used {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.capacity-text {
  font-size: 12px;
  color: #666;
}

.warehouse-stats {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
  padding: 15px;
  background: #f9f9f9;
  border-bottom: 1px solid #eee;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-value {
  font-weight: 700;
  color: #667eea;
  font-size: 16px;
}

.stat-label {
  font-size: 11px;
  color: #999;
  text-transform: uppercase;
}

.warehouse-actions {
  display: flex;
  gap: 8px;
  padding: 12px 15px;
}

.btn-view,
.btn-edit {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  font-size: 12px;
}

.btn-view {
  background: #3498db;
  color: white;
}

.btn-view:hover {
  background: #2980b9;
}

.btn-edit {
  background: #95a5a6;
  color: white;
}

.btn-edit:hover {
  background: #7f8c8d;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 28px;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.btn-secondary {
  flex: 1;
  padding: 10px;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.loading {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 8px;
}
</style>
