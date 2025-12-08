<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>📋 Inventory Items</h1>
        <button @click="goToCreateItem" class="btn-primary">+ New Item</button>
      </div>

      <div class="filters">
        <input
          v-model="filters.search"
          placeholder="Search by SKU or name..."
          class="filter-input"
          @input="applyFilters"
        />
        <select v-model="filters.category" class="filter-select" @change="applyFilters">
          <option value="">All Categories</option>
          <option v-for="cat in categories" :key="cat" :value="cat">
            {{ cat }}
          </option>
        </select>
        <select v-model="filters.warehouse_id" class="filter-select" @change="applyFilters">
          <option value="">All Warehouses</option>
          <option v-for="wh in warehouses" :key="wh.id" :value="wh.id">
            {{ wh.name }}
          </option>
        </select>
      </div>

      <div v-if="loading" class="loading">Loading items...</div>

      <div v-else-if="items.length === 0" class="empty-state">
        <p>No items found. Create your first item!</p>
      </div>

      <div v-else class="items-table">
        <table>
          <thead>
            <tr>
              <th>SKU</th>
              <th>Name</th>
              <th>Category</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Reorder Level</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id" :class="{ lowStock: item.current_stock <= item.reorder_level }">
              <td class="sku">{{ item.sku }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.category || 'N/A' }}</td>
              <td>${{ formatPrice(item.unit_price) }}</td>
              <td class="stock-level">{{ item.current_stock }}</td>
              <td>{{ item.reorder_level }}</td>
              <td>
                <span class="status-badge" :class="item.current_stock <= item.reorder_level ? 'low' : 'ok'">
                  {{ item.current_stock <= item.reorder_level ? 'Low Stock' : 'OK' }}
                </span>
              </td>
              <td class="actions">
                <button @click="viewItem(item.id)" class="btn-small btn-view">View</button>
                <button @click="editItem(item.id)" class="btn-small btn-edit">Edit</button>
                <button @click="deleteItem(item.id)" class="btn-small btn-delete">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="totalPages > 1" class="pagination">
        <button
          v-for="page in totalPages"
          :key="page"
          @click="goToPage(page)"
          :class="{ active: currentPage === page }"
          class="page-btn"
        >
          {{ page }}
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import { inventoryService } from '../services/inventoryService'

const router = useRouter()
const items = ref([])
const warehouses = ref([])
const categories = ref([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)

const filters = ref({
  search: '',
  category: '',
  warehouse_id: ''
})

const loadItems = async (page = 1) => {
  try {
    loading.value = true
    const response = await inventoryService.getItems(page, 10, {
      category: filters.value.category || undefined,
      warehouse_id: filters.value.warehouse_id || undefined
    })
    
    let itemList = response.data.items
    if (filters.value.search) {
      itemList = itemList.filter(item =>
        item.sku.toLowerCase().includes(filters.value.search.toLowerCase()) ||
        item.name.toLowerCase().includes(filters.value.search.toLowerCase())
      )
    }
    
    items.value = itemList
    currentPage.value = response.data.current_page
    totalPages.value = response.data.pages
    
    // Extract categories from items
    const cats = new Set(items.value.map(i => i.category).filter(c => c))
    categories.value = Array.from(cats)
  } catch (error) {
    console.error('Failed to load items:', error)
    alert('Failed to load items')
  } finally {
    loading.value = false
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

const formatPrice = (price) => {
  return parseFloat(price).toFixed(2)
}

const applyFilters = () => {
  currentPage.value = 1
  loadItems(1)
}

const goToPage = (page) => {
  loadItems(page)
}

const goToCreateItem = () => {
  router.push('/inventory/new')
}

const viewItem = (id) => {
  router.push(`/inventory/${id}`)
}

const editItem = (id) => {
  router.push(`/inventory/${id}/edit`)
}

const deleteItem = async (id) => {
  if (!confirm('Are you sure you want to delete this item?')) return
  
  try {
    // Item deletion would need to be implemented in the service
    alert('Item deleted')
    loadItems(currentPage.value)
  } catch (error) {
    console.error('Failed to delete item:', error)
    alert('Failed to delete item')
  }
}

onMounted(() => {
  loadWarehouses()
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
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-input,
.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.filter-input {
  flex: 1;
  min-width: 200px;
}

.items-table {
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

tr.lowStock {
  background-color: #fff3cd;
}

.sku {
  font-weight: 600;
  font-family: monospace;
  color: #333;
}

.stock-level {
  font-weight: 600;
  color: #27ae60;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.ok {
  background: #d4edda;
  color: #27ae60;
}

.status-badge.low {
  background: #fff3cd;
  color: #f39c12;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-small {
  padding: 5px 10px;
  font-size: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-view {
  background: #3498db;
  color: white;
}

.btn-view:hover {
  background: #2980b9;
}

.btn-edit {
  background: #f39c12;
  color: white;
}

.btn-edit:hover {
  background: #e67e22;
}

.btn-delete {
  background: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background: #c0392b;
}

.pagination {
  display: flex;
  gap: 5px;
  margin-top: 20px;
  justify-content: center;
}

.page-btn {
  padding: 8px 12px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 4px;
}

.page-btn.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.loading,
.empty-state {
  text-align: center;
  padding: 40px 20px;
  background: white;
  border-radius: 8px;
}
</style>
