<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>📤 Sale Orders</h1>
        <button @click="showCreateForm = true" class="btn-primary">+ New SO</button>
      </div>

      <div class="filters">
        <select v-model="filters.status" class="filter-select" @change="loadOrders()">
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="fulfilled">Fulfilled</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>

      <div v-if="loading" class="loading">Loading orders...</div>

      <div v-else class="orders-table">
        <table>
          <thead>
            <tr>
              <th>SO Number</th>
              <th>Customer</th>
              <th>Item</th>
              <th>Quantity</th>
              <th>Unit Price</th>
              <th>Total</th>
              <th>Status</th>
              <th>Order Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="so in orders" :key="so.id">
              <td class="so-number">{{ so.so_number }}</td>
              <td>{{ so.customer_name }}</td>
              <td>{{ so.item_name }}</td>
              <td>{{ so.quantity }}</td>
              <td>${{ formatPrice(so.unit_price) }}</td>
              <td class="amount">${{ formatPrice(so.total_price) }}</td>
              <td><span class="status-badge" :class="so.status">{{ so.status }}</span></td>
              <td>{{ formatDate(so.order_date) }}</td>
              <td class="actions">
                <button 
                  v-if="so.status === 'pending'"
                  @click="fulfillSO(so.id)"
                  class="btn-small btn-success"
                >
                  Fulfill
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Create SO Modal -->
      <div v-if="showCreateForm" class="modal-overlay" @click="showCreateForm = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>Create Sale Order</h2>
            <button @click="showCreateForm = false" class="btn-close">×</button>
          </div>
          
          <form @submit.prevent="createSO" class="form">
            <div class="form-group">
              <label>SO Number</label>
              <input v-model="soForm.so_number" required />
            </div>
            
            <div class="form-group">
              <label>Customer</label>
              <input v-model="soForm.customer_name" required />
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label>Item</label>
                <select v-model="soForm.item_id" required>
                  <option value="">Select Item</option>
                  <option v-for="item in items" :key="item.id" :value="item.id">
                    {{ item.sku }} - {{ item.name }} (Stock: {{ item.current_stock }})
                  </option>
                </select>
              </div>
              
              <div class="form-group">
                <label>Quantity</label>
                <input v-model.number="soForm.quantity" type="number" required />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label>Unit Price</label>
                <input v-model.number="soForm.unit_price" type="number" step="0.01" required />
              </div>
              
              <div class="form-group">
                <label>Expected Delivery</label>
                <input v-model="soForm.expected_delivery_date" type="date" />
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

const filters = ref({
  status: ''
})

const soForm = ref({
  so_number: '',
  customer_name: '',
  item_id: '',
  quantity: 0,
  unit_price: 0,
  expected_delivery_date: ''
})

const loadOrders = async () => {
  try {
    loading.value = true
    const response = await inventoryService.getSaleOrders(1, 100, { status: filters.value.status || undefined })
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

const formatPrice = (price) => parseFloat(price).toFixed(2)
const formatDate = (date) => new Date(date).toLocaleDateString()

const createSO = async () => {
  try {
    await inventoryService.createSaleOrder(soForm.value)
    showCreateForm.value = false
    soForm.value = {
      so_number: '',
      customer_name: '',
      item_id: '',
      quantity: 0,
      unit_price: 0,
      expected_delivery_date: ''
    }
    await loadOrders()
  } catch (error) {
    console.error('Failed to create SO:', error)
    alert('Failed to create sale order')
  }
}

const fulfillSO = async (id) => {
  try {
    await inventoryService.fulfillSaleOrder(id)
    alert('Sale order fulfilled')
    await loadOrders()
  } catch (error) {
    console.error('Failed to fulfill SO:', error)
    alert('Failed to fulfill sale order')
  }
}

onMounted(() => {
  loadOrders()
  loadItems()
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

.so-number {
  font-weight: 600;
  color: #9b59b6;
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

.status-badge.fulfilled {
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
