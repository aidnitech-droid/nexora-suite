<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>{{ isEdit ? 'Edit Expense' : 'Create New Expense' }}</h1>
        <button @click="goBack" class="btn-secondary">← Back</button>
      </div>

      <div class="form-container">
        <form @submit.prevent="submitForm" class="form">
          <div class="form-group">
            <label for="title">Title *</label>
            <input
              id="title"
              v-model="form.title"
              type="text"
              placeholder="Expense title"
              required
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="amount">Amount *</label>
              <input
                id="amount"
                v-model.number="form.amount"
                type="number"
                step="0.01"
                placeholder="0.00"
                required
              />
            </div>

            <div class="form-group">
              <label for="category">Category</label>
              <select id="category" v-model.number="form.category_id">
                <option :value="null">Select a category</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="date">Date</label>
              <input
                id="date"
                v-model="form.date"
                type="date"
              />
            </div>

            <div class="form-group">
              <label for="status">Status</label>
              <select id="status" v-model="form.status">
                <option value="draft">Draft</option>
                <option value="submitted">Submitted</option>
                <option value="approved">Approved</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              id="description"
              v-model="form.description"
              placeholder="Add description..."
              rows="4"
            ></textarea>
          </div>

          <div class="form-group">
            <label>Attachments</label>
            <div class="file-upload">
              <input
                type="file"
                @change="onFileSelected"
                multiple
                accept=".jpg,.jpeg,.png,.gif,.pdf,.doc,.docx,.xls,.xlsx"
              />
              <span class="upload-text">Drag files here or click to select (Images, PDF, Office docs)</span>
            </div>

            <div v-if="existingAttachments.length > 0" class="attachments-list">
              <h4>Current Attachments</h4>
              <div v-for="att in existingAttachments" :key="att.id" class="attachment-item">
                <span>{{ att.filename }}</span>
                <button @click="removeAttachment(att.id)" type="button" class="btn-remove">×</button>
              </div>
            </div>

            <div v-if="selectedFiles.length > 0" class="selected-files">
              <h4>Files to Upload</h4>
              <div v-for="(file, idx) in selectedFiles" :key="idx" class="file-item">
                <span>{{ file.name }}</span>
                <button @click="removeFile(idx)" type="button" class="btn-remove">×</button>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">{{ isEdit ? 'Update' : 'Create' }}</button>
            <button type="button" @click="goBack" class="btn-secondary">Cancel</button>
          </div>
        </form>
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
const isEdit = ref(!!route.params.id)

const form = ref({
  title: '',
  amount: 0,
  category_id: null,
  date: new Date().toISOString().split('T')[0],
  status: 'draft',
  description: ''
})

const categories = ref([])
const selectedFiles = ref([])
const existingAttachments = ref([])

const loadCategories = async () => {
  try {
    const response = await expenseService.getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('Failed to load categories:', error)
  }
}

const loadExpense = async (id) => {
  try {
    const response = await expenseService.getExpense(id)
    const expense = response.data
    form.value = {
      title: expense.title,
      amount: expense.amount,
      category_id: expense.category_id,
      date: new Date(expense.date).toISOString().split('T')[0],
      status: expense.status,
      description: expense.description
    }
    existingAttachments.value = expense.attachments || []
  } catch (error) {
    console.error('Failed to load expense:', error)
    alert('Failed to load expense')
    router.push('/expenses')
  }
}

const onFileSelected = (event) => {
  selectedFiles.value = Array.from(event.target.files)
}

const removeFile = (idx) => {
  selectedFiles.value.splice(idx, 1)
}

const removeAttachment = async (attId) => {
  try {
    await expenseService.deleteAttachment(attId)
    existingAttachments.value = existingAttachments.value.filter(a => a.id !== attId)
  } catch (error) {
    console.error('Failed to delete attachment:', error)
    alert('Failed to delete attachment')
  }
}

const uploadFiles = async (expenseId) => {
  if (selectedFiles.value.length === 0) return

  for (const file of selectedFiles.value) {
    try {
      const formData = new FormData()
      formData.append('file', file)
      await expenseService.uploadAttachment(expenseId, formData)
    } catch (error) {
      console.error('Failed to upload file:', error)
      alert(`Failed to upload ${file.name}`)
    }
  }
}

const submitForm = async () => {
  try {
    if (isEdit.value) {
      await expenseService.updateExpense(route.params.id, form.value)
    } else {
      const response = await expenseService.createExpense(form.value)
      if (selectedFiles.value.length > 0) {
        await uploadFiles(response.data.id)
      }
    }

    if (selectedFiles.value.length > 0) {
      await uploadFiles(route.params.id || route.params.expenseId)
    }

    alert('Expense saved successfully')
    router.push('/expenses')
  } catch (error) {
    console.error('Failed to save expense:', error)
    alert('Failed to save expense')
  }
}

const goBack = () => {
  router.push('/expenses')
}

onMounted(() => {
  loadCategories()
  if (isEdit.value) {
    loadExpense(route.params.id)
  }
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

.form-container {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 600px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.file-upload {
  border: 2px dashed #3498db;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  background: #ecf0f1;
  transition: all 0.3s;
}

.file-upload:hover {
  border-color: #2980b9;
  background: #d5dbdb;
}

.file-upload input {
  display: none;
}

.upload-text {
  color: #666;
  font-size: 14px;
}

.attachments-list,
.selected-files {
  margin-top: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
}

.attachments-list h4,
.selected-files h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #333;
}

.attachment-item,
.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  background: white;
  border-radius: 4px;
  margin-bottom: 8px;
}

.attachment-item span,
.file-item span {
  font-size: 14px;
  color: #555;
  word-break: break-word;
}

.btn-remove {
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-weight: bold;
  flex-shrink: 0;
}

.btn-remove:hover {
  background: #c0392b;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-primary {
  flex: 1;
  padding: 12px;
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

.btn-secondary {
  flex: 1;
}
</style>
