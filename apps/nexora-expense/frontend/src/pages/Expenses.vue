<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>Expenses</h1>
        <button @click="goToCreateExpense" class="btn-primary">+ New Expense</button>
      </div>

      <div class="filters">
        <input
          v-model="filters.title"
          placeholder="Search by title..."
          class="filter-input"
          @input="applyFilters"
        />
        <select v-model="filters.status" class="filter-select" @change="applyFilters">
          <option value="">All Status</option>
          <option value="draft">Draft</option>
          <option value="submitted">Submitted</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
        </select>
        <select v-model="filters.category_id" class="filter-select" @change="applyFilters">
          <option value="">All Categories</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
      </div>

      <div v-if="loading" class="loading">Loading expenses...</div>

      <div v-else-if="expenses.length === 0" class="empty-state">
        <p>No expenses found. Create your first expense!</p>
      </div>

      <div v-else class="expenses-table">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Amount</th>
              <th>Category</th>
              <th>Status</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="expense in expenses" :key="expense.id" :class="expense.status">
              <td>{{ expense.title }}</td>
              <td class="amount">${{ formatAmount(expense.amount) }}</td>
              <td>{{ getCategoryName(expense.category_id) }}</td>
              <td><span class="status-badge" :class="expense.status">{{ expense.status }}</span></td>
              <td>{{ formatDate(expense.date) }}</td>
              <td class="actions">
                <button @click="viewExpense(expense.id)" class="btn-small btn-view">View</button>
                <button @click="editExpense(expense.id)" class="btn-small btn-edit">Edit</button>
                <button @click="deleteExpense(expense.id)" class="btn-small btn-delete">Delete</button>
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import { expenseService } from '../services/expenseService'

const router = useRouter()
const expenses = ref([])
const categories = ref([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)

const filters = ref({
  title: '',
  status: '',
  category_id: ''
})

const loadExpenses = async (page = 1) => {
  try {
    loading.value = true
    const response = await expenseService.getExpenses(page, 10, {
      status: filters.value.status || undefined,
      category_id: filters.value.category_id || undefined
    })
    
    expenses.value = response.data.expenses.filter(e =>
      e.title.toLowerCase().includes(filters.value.title.toLowerCase())
    )
    currentPage.value = response.data.current_page
    totalPages.value = response.data.pages
  } catch (error) {
    console.error('Failed to load expenses:', error)
    alert('Failed to load expenses')
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const response = await expenseService.getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('Failed to load categories:', error)
  }
}

const formatAmount = (amount) => {
  return parseFloat(amount).toFixed(2)
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

const getCategoryName = (categoryId) => {
  const cat = categories.value.find(c => c.id === categoryId)
  return cat ? cat.name : 'Uncategorized'
}

const applyFilters = () => {
  currentPage.value = 1
  loadExpenses(1)
}

const goToPage = (page) => {
  loadExpenses(page)
}

const goToCreateExpense = () => {
  router.push('/expenses/new')
}

const viewExpense = (id) => {
  router.push(`/expenses/${id}`)
}

const editExpense = (id) => {
  router.push(`/expenses/${id}/edit`)
}

const deleteExpense = async (id) => {
  if (!confirm('Are you sure you want to delete this expense?')) return
  
  try {
    await expenseService.deleteExpense(id)
    alert('Expense deleted successfully')
    loadExpenses(currentPage.value)
  } catch (error) {
    console.error('Failed to delete expense:', error)
    alert('Failed to delete expense')
  }
}

onMounted(() => {
  loadCategories()
  loadExpenses()
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

.expenses-table {
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

.status-badge.draft {
  background: #e8f4f8;
  color: #3498db;
}

.status-badge.submitted {
  background: #fff3cd;
  color: #f39c12;
}

.status-badge.approved {
  background: #d4edda;
  color: #27ae60;
}

.status-badge.rejected {
  background: #f8d7da;
  color: #e74c3c;
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

.loading {
  color: #666;
}

.empty-state {
  color: #999;
}
</style>
