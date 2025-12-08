<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>📝 {{ editingId ? 'Edit Item' : 'Create Item' }}</h1>
        <router-link to="/inventory" class="btn-back">← Back to Inventory</router-link>
      </div>

      <div class="form-container">
        <form @submit.prevent="saveItem" class="item-form">
          <!-- Basic Information -->
          <fieldset class="form-section">
            <legend>Basic Information</legend>
            
            <div class="form-row">
              <div class="form-group">
                <label for="sku">SKU *</label>
                <input 
                  id="sku"
                  v-model="itemForm.sku" 
                  required
                  :readonly="!!editingId"
                  placeholder="e.g., SKU-001"
                />
              </div>
              
              <div class="form-group">
                <label for="name">Item Name *</label>
                <input 
                  id="name"
                  v-model="itemForm.name" 
                  required
                  placeholder="Item name"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="description">Description</label>
              <textarea 
                id="description"
                v-model="itemForm.description"
                rows="3"
                placeholder="Item description"
              ></textarea>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="category">Category *</label>
                <input 
                  id="category"
                  v-model="itemForm.category" 
                  required
                  placeholder="e.g., Electronics"
                />
              </div>
              
              <div class="form-group">
                <label for="warehouse">Warehouse *</label>
                <select v-model="itemForm.warehouse_id" required>
                  <option value="">Select Warehouse</option>
                  <option v-for="wh in warehouses" :key="wh.id" :value="wh.id">
                    {{ wh.name }}
                  </option>
                </select>
              </div>
            </div>
          </fieldset>

          <!-- Pricing Information -->
          <fieldset class="form-section">
            <legend>Pricing</legend>
            
            <div class="form-row">
              <div class="form-group">
                <label for="unitPrice">Unit Price *</label>
                <input 
                  id="unitPrice"
                  v-model.number="itemForm.unit_price" 
                  type="number"
                  step="0.01"
                  required
                  placeholder="0.00"
                />
              </div>
              
              <div class="form-group">
                <label for="currentStock">Current Stock *</label>
                <input 
                  id="currentStock"
                  v-model.number="itemForm.current_stock" 
                  type="number"
                  required
                  placeholder="0"
                />
              </div>
            </div>
          </fieldset>

          <!-- Stock Management -->
          <fieldset class="form-section">
            <legend>Stock Management</legend>
            
            <div class="form-row">
              <div class="form-group">
                <label for="reorderLevel">Reorder Level *</label>
                <input 
                  id="reorderLevel"
                  v-model.number="itemForm.reorder_level" 
                  type="number"
                  required
                  placeholder="Minimum stock level"
                />
                <small>Alert triggered when stock falls below this level</small>
              </div>
              
              <div class="form-group">
                <label for="reorderQty">Reorder Quantity *</label>
                <input 
                  id="reorderQty"
                  v-model.number="itemForm.reorder_quantity" 
                  type="number"
                  required
                  placeholder="Quantity to order"
                />
              </div>
            </div>
          </fieldset>

          <!-- Form Actions -->
          <div class="form-actions">
            <button type="submit" class="btn-primary">
              {{ editingId ? 'Update Item' : 'Create Item' }}
            </button>
            <button type="button" @click="cancelForm" class="btn-secondary">
              Cancel
            </button>
            <button 
              v-if="editingId"
              type="button" 
              @click="deleteItem"
              class="btn-danger"
            >
              Delete Item
            </button>
          </div>
        </form>

        <!-- Form Info -->
        <aside class="form-info">
          <div class="info-card">
            <h3>💡 Tips</h3>
            <ul>
              <li>SKU must be unique</li>
              <li>Reorder level should be based on average usage</li>
              <li>Set appropriate warehouse location</li>
              <li>All fields marked with * are required</li>
            </ul>
          </div>

          <div v-if="editingId" class="info-card">
            <h3>📊 Current Status</h3>
            <div class="status-info">
              <div class="status-item">
                <span class="status-label">Stock Level:</span>
                <span class="status-value">{{ itemForm.current_stock }}</span>
              </div>
              <div class="status-item">
                <span class="status-label">Reorder Level:</span>
                <span class="status-value">{{ itemForm.reorder_level }}</span>
              </div>
              <div class="status-item">
                <span class="status-label">Status:</span>
                <span class="status-value">
                  <span 
                    class="status-badge"
                    :class="itemForm.current_stock >= itemForm.reorder_level ? 'ok' : 'warning'"
                  >
                    {{ itemForm.current_stock >= itemForm.reorder_level ? 'Normal' : 'Low Stock' }}
                  </span>
                </span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import { inventoryService } from '../services/inventoryService'

const router = useRouter()
const route = useRoute()

const editingId = ref(null)
const warehouses = ref([])

const itemForm = ref({
  sku: '',
  name: '',
  description: '',
  category: '',
  unit_price: 0,
  reorder_level: 0,
  reorder_quantity: 0,
  warehouse_id: '',
  current_stock: 0
})

const loadWarehouses = async () => {
  try {
    const response = await inventoryService.getWarehouses()
    warehouses.value = response.data
  } catch (error) {
    console.error('Failed to load warehouses:', error)
  }
}

const loadItem = async () => {
  const id = route.params.id
  if (id) {
    try {
      const response = await inventoryService.getItem(id)
      const item = response.data
      itemForm.value = {
        sku: item.sku,
        name: item.name,
        description: item.description,
        category: item.category,
        unit_price: item.unit_price,
        reorder_level: item.reorder_level,
        reorder_quantity: item.reorder_quantity,
        warehouse_id: item.warehouse_id,
        current_stock: item.current_stock
      }
      editingId.value = id
    } catch (error) {
      console.error('Failed to load item:', error)
      alert('Failed to load item')
      router.push('/inventory')
    }
  }
}

const saveItem = async () => {
  try {
    if (editingId.value) {
      await inventoryService.updateItem(editingId.value, itemForm.value)
      alert('Item updated successfully')
    } else {
      await inventoryService.createItem(itemForm.value)
      alert('Item created successfully')
    }
    router.push('/inventory')
  } catch (error) {
    console.error('Failed to save item:', error)
    alert('Failed to save item: ' + (error.response?.data?.message || error.message))
  }
}

const deleteItem = async () => {
  if (confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
    try {
      await inventoryService.deleteItem(editingId.value)
      alert('Item deleted successfully')
      router.push('/inventory')
    } catch (error) {
      console.error('Failed to delete item:', error)
      alert('Failed to delete item')
    }
  }
}

const cancelForm = () => {
  router.push('/inventory')
}

onMounted(() => {
  loadWarehouses()
  loadItem()
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

.btn-back {
  padding: 8px 16px;
  background: #95a5a6;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
}

.btn-back:hover {
  background: #7f8c8d;
}

.form-container {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 20px;
}

.item-form {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 30px;
  padding-bottom: 30px;
  border-bottom: 1px solid #eee;
  border: none;
}

.form-section:last-of-type {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.form-section legend {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
  display: block;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-group input:readonly {
  background: #f5f5f5;
  cursor: not-allowed;
}

.form-group small {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn-primary {
  flex: 1;
  padding: 12px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 700;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-secondary {
  flex: 1;
  padding: 12px 20px;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 700;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.btn-danger {
  flex: 1;
  padding: 12px 20px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 700;
}

.btn-danger:hover {
  background: #c0392b;
}

.form-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.info-card h3 {
  margin: 0 0 15px 0;
  font-size: 14px;
  color: #333;
}

.info-card ul {
  margin: 0;
  padding-left: 20px;
  list-style: none;
}

.info-card li {
  font-size: 13px;
  color: #666;
  margin-bottom: 8px;
  position: relative;
  padding-left: 16px;
}

.info-card li:before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #27ae60;
  font-weight: bold;
}

.status-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.status-item:last-child {
  border-bottom: none;
}

.status-label {
  font-size: 12px;
  color: #999;
  font-weight: 600;
}

.status-value {
  font-size: 14px;
  color: #333;
  font-weight: 600;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}

.status-badge.ok {
  background: #d4edda;
  color: #27ae60;
}

.status-badge.warning {
  background: #fff3cd;
  color: #f39c12;
}

@media (max-width: 768px) {
  .form-container {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
