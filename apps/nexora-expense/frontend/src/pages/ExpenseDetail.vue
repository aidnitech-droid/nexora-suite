<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>Expense Details</h1>
        <button @click="goBack" class="btn-secondary">← Back</button>
      </div>

      <div v-if="loading" class="loading">Loading expense...</div>

      <div v-else-if="expense" class="detail-container">
        <div class="detail-card">
          <div class="detail-header">
            <div>
              <h2>{{ expense.title }}</h2>
              <p class="expense-id">ID: {{ expense.id }}</p>
            </div>
            <div class="header-actions">
              <button @click="editExpense" class="btn-primary">Edit</button>
              <button @click="deleteExpense" class="btn-danger">Delete</button>
            </div>
          </div>

          <div class="detail-grid">
            <div class="detail-item">
              <span class="label">Amount</span>
              <span class="value amount">${{ formatAmount(expense.amount) }}</span>
            </div>

            <div class="detail-item">
              <span class="label">Category</span>
              <span class="value">{{ getCategoryName(expense.category_id) }}</span>
            </div>

            <div class="detail-item">
              <span class="label">Status</span>
              <span class="value status-badge" :class="expense.status">{{ expense.status }}</span>
            </div>

            <div class="detail-item">
              <span class="label">Date</span>
              <span class="value">{{ formatDate(expense.date) }}</span>
            </div>

            <div class="detail-item">
              <span class="label">Created</span>
              <span class="value">{{ formatDate(expense.created_at) }}</span>
            </div>
          </div>

          <div v-if="expense.description" class="description-section">
            <h3>Description</h3>
            <p>{{ expense.description }}</p>
          </div>

          <div v-if="expense.attachments && expense.attachments.length > 0" class="attachments-section">
            <h3>Attachments</h3>
            <div class="attachments-list">
              <div v-for="att in expense.attachments" :key="att.id" class="attachment-card">
                <div class="attachment-info">
                  <span class="filename">📎 {{ att.filename }}</span>
                </div>
                <div class="attachment-actions">
                  <a :href="att.url" download class="btn-download">Download</a>
                  <button @click="deleteAttachment(att.id)" class="btn-small btn-delete">Delete</button>
                </div>
              </div>
            </div>
          </div>

          <div class="detail-footer">
            <button @click="goBack" class="btn-secondary">Back to List</button>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <p>Expense not found</p>
        <button @click="goBack" class="btn-primary">Go Back</button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import { expenseService } from '../services/expenseService'

const router = useRouter()
const route = useRoute()
const expense = ref(null)
const categories = ref([])
const loading = ref(false)

const loadExpense = async () => {
  try {
    loading.value = true
    const response = await expenseService.getExpense(route.params.id)
    expense.value = response.data
  } catch (error) {
    console.error('Failed to load expense:', error)
    alert('Failed to load expense')
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

const getCategoryName = (categoryId) => {
  if (!categoryId) return 'Uncategorized'
  const cat = categories.value.find(c => c.id === categoryId)
  return cat ? cat.name : 'Uncategorized'
}

const formatAmount = (amount) => {
  return parseFloat(amount).toFixed(2)
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

const editExpense = () => {
  router.push(`/expenses/${expense.value.id}/edit`)
}

const deleteAttachment = async (attId) => {
  if (!confirm('Delete this attachment?')) return

  try {
    await expenseService.deleteAttachment(attId)
    expense.value.attachments = expense.value.attachments.filter(a => a.id !== attId)
    alert('Attachment deleted')
  } catch (error) {
    console.error('Failed to delete attachment:', error)
    alert('Failed to delete attachment')
  }
}

const deleteExpense = async () => {
  if (!confirm('Are you sure you want to delete this expense?')) return

  try {
    await expenseService.deleteExpense(route.params.id)
    alert('Expense deleted successfully')
    router.push('/expenses')
  } catch (error) {
    console.error('Failed to delete expense:', error)
    alert('Failed to delete expense')
  }
}

const goBack = () => {
  router.push('/expenses')
}

onMounted(() => {
  loadCategories()
  loadExpense()
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

.btn-secondary {
  padding: 8px 16px;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.detail-container {
  max-width: 800px;
  margin: 0 auto;
}

.detail-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #eee;
}

.detail-header h2 {
  margin: 0 0 5px 0;
  font-size: 28px;
  color: #333;
}

.expense-id {
  margin: 0;
  color: #999;
  font-size: 12px;
}

.header-actions {
  display: flex;
  gap: 10px;
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

.btn-danger {
  padding: 10px 20px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.btn-danger:hover {
  background: #c0392b;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item .label {
  font-weight: 600;
  color: #666;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-item .value {
  font-size: 16px;
  color: #333;
}

.amount {
  font-weight: 700;
  color: #27ae60;
  font-size: 24px;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  width: fit-content;
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

.description-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.description-section h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.description-section p {
  margin: 0;
  color: #666;
  line-height: 1.6;
  white-space: pre-wrap;
}

.attachments-section {
  margin-bottom: 30px;
}

.attachments-section h3 {
  margin: 0 0 15px 0;
  color: #333;
}

.attachments-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.attachment-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 6px;
}

.attachment-info {
  flex: 1;
}

.filename {
  color: #333;
  font-weight: 500;
  word-break: break-all;
}

.attachment-actions {
  display: flex;
  gap: 8px;
  margin-left: 15px;
  flex-shrink: 0;
}

.btn-download {
  padding: 6px 12px;
  background: #27ae60;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-size: 12px;
  border: none;
  cursor: pointer;
}

.btn-download:hover {
  background: #229954;
}

.btn-delete {
  padding: 6px 12px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.btn-delete:hover {
  background: #c0392b;
}

.btn-small {
  padding: 5px 10px;
}

.detail-footer {
  padding-top: 20px;
  border-top: 2px solid #eee;
}

.loading,
.empty-state {
  text-align: center;
  padding: 40px 20px;
  background: white;
  border-radius: 8px;
}

.empty-state p {
  color: #999;
  margin-bottom: 20px;
}
</style>
