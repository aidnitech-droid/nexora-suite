<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>📥 Purchase Orders</h1>
        <button @click="showCreateForm = true" class="btn-primary">+ New PO</button>
      </div>

      <div class="filters">
        <select v-model="filters.status" class="filter-select" @change="loadOrders()">
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="received">Received</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>

      <div v-if="loading" class="loading">Loading orders...</div>

      <div v-else class="orders-table">
        <table>
          <thead>
            <tr>
              <th>PO Number</th>
              <th>Supplier</th>
              <th>Item</th>
              <th>Quantity</th>
              <th>Unit Cost</th>
              <th>Total</th>
              <th>Status</th>
              <th>Order Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="po in orders" :key="po.id">
              <td class="po-number">{{ po.po_number }}</td>
              <td>{{ po.supplier_name }}</td>
              <td>{{ po.item_name }}</td>
              <td>{{ po.quantity }}</td>
              <td>${{ formatPrice(po.unit_cost) }}</td>
              <td class="amount">${{ formatPrice(po.total_cost) }}</td>
              <td><span class="status-badge" :class="po.status">{{ po.status }}</span></td>
              <td>{{ formatDate(po.order_date) }}</td>
              <td class="actions">
                <button 
                  v-if="po.status === 'pending'"
                  @click="receivePO(po.id)"
                  class="btn-small btn-success"
                >
                  Receive
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Create PO Modal -->
      <div v-if="showCreateForm" class="modal-overlay" @click="showCreateForm = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>Create Purchase Order</h2>
            <button @click="showCreateForm = false" class="btn-close">×</button>
          </div>
          
          <form @submit.prevent="createPO" class="form">
            <div class="form-group">
              <label>PO Number</label>
              <input v-model="poForm.po_number" required />
            </div>
            
            <div class="form-group">
              <label>Supplier</label>
              <input v-model="poForm.supplier_name" required />
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label>Item</label>
                <select v-model="poForm.item_id" required>
                  <option value="">Select Item</option>
                  <option v-for="item in items" :key="item.id" :value="item.id">
                    {{ item.sku }} - {{ item.name }}
                  </option>
                </select>
              </div>
              
              <div class="form-group">
                <label>Warehouse</label>
                <select v-model="poForm.warehouse_id" required>
                  <option value="">Select Warehouse</option>
                  <option v-for="wh in warehouses" :key="wh.id" :value="wh.id">
                    {{ wh.name }}
                  </option>
                </select>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label>Quantity</label>
                <input v-model.number="poForm.quantity" type="number" required />
              </div>
              
              <div class="form-group">
                <label>Unit Cost</label>
                <input v-model.number="poForm.unit_cost" type="number" step="0.01" required />
              </div>
            </div>
            
            <div class="form-actions">
              <button type="submit" class="btn-primary">Create</button>
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
const orders = ref([])
const items = ref([])
const warehouses = ref([])

const filters = ref({
  status: ''
})

const poForm = ref({
  po_number: '',
  supplier_name: '',
  item_id: '',
  warehouse_id: '',
  quantity: 0,
  unit_cost: 0
})

const loadOrders = async () => {
  try {
    loading.value = true
    const response = await inventoryService.getPurchaseOrders(1, 100, { status: filters.value.status || undefined })
    orders.value = response.data.orders
  } catch (error) {
    console.error('Failed to load orders:', error)
  } finally {
    loading.value = false
  }
}

const loadItems = async () => {
  try {
    const response = await inventoryService.getItems(1, 1000)
    items.value = response.data.items
  } catch (error) {
    console.error('Failed to load items:', error)
  }
}

const loadWarehouses = async () => {
  try {
    const response = await inventoryService.getWarehouses()
    warehouses.value = response.data
  } catch (error) {
    console.error('Failed to load warehouses:', error)
  }
}

const formatPrice = (price) => parseFloat(price).toFixed(2)
const formatDate = (date) => new Date(date).toLocaleDateString()

const createPO = async () => {
  try {
    await inventoryService.createPurchaseOrder(poForm.value)
    showCreateForm.value = false
    poForm.value = {
      po_number: '',
      supplier_name: '',
      item_id: '',
      warehouse_id: '',
      quantity: 0,
      unit_cost: 0
    }
    await loadOrders()
  } catch (error) {
    console.error('Failed to create PO:', error)
    alert('Failed to create purchase order')
  }
}

const receivePO = async (id) => {
  try {
    await inventoryService.receivePurchaseOrder(id)
    alert('Purchase order received')
    await loadOrders()
  } catch (error) {
    console.error('Failed to receive PO:', error)
    alert('Failed to receive purchase order')
  }
}

onMounted(() => {
  loadOrders()
  loadItems()
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

.filters {
  margin-bottom: 20px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.orders-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: #f8f9fa;
  padding: 15px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
}

td {
  padding: 15px;
  border-bottom: 1px solid #dee2e6;
}

tr:hover {
  background: #f8f9fa;
}

.po-number {
  font-weight: 600;
  color: #3498db;
}

.amount {
  font-weight: 600;
  color: #27ae60;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.pending {
  background: #fff3cd;
  color: #f39c12;
}

.status-badge.received {
  background: #d4edda;
  color: #27ae60;
}

.status-badge.cancelled {
  background: #f8d7da;
  color: #e74c3c;
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

.btn-success {
  background: #27ae60;
  color: white;
}

.btn-success:hover {
  background: #229954;
}

.btn-small {
  padding: 5px 10px;
  font-size: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.loading {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 8px;
}
</style>
