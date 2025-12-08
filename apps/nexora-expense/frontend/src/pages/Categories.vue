<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>Categories</h1>
        <button @click="showCreateForm" class="btn-primary">+ New Category</button>
      </div>

      <div v-if="loading" class="loading">Loading categories...</div>

      <div v-else class="categories-grid">
        <div v-for="category in categories" :key="category.id" class="category-card">
          <div class="card-header">
            <h3>{{ category.name }}</h3>
            <div class="card-actions">
              <button @click="editCategory(category)" class="btn-small btn-edit">Edit</button>
              <button @click="deleteCategory(category.id)" class="btn-small btn-delete">Delete</button>
            </div>
          </div>
          <p class="category-description">{{ category.description || 'No description' }}</p>
          <span class="created-date">{{ formatDate(category.created_at) }}</span>
        </div>
      </div>

      <div v-if="categories.length === 0 && !loading" class="empty-state">
        <p>No categories yet. Create your first one!</p>
      </div>

      <!-- Modal Form -->
      <div v-if="showForm" class="modal-overlay" @click="closeForm">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ editingId ? 'Edit Category' : 'Create New Category' }}</h2>
            <button @click="closeForm" class="btn-close">×</button>
          </div>

          <form @submit.prevent="submitForm" class="form">
            <div class="form-group">
              <label for="name">Category Name *</label>
              <input
                id="name"
                v-model="formData.name"
                type="text"
                placeholder="e.g., Travel, Meals, Office"
                required
              />
            </div>

            <div class="form-group">
              <label for="description">Description</label>
              <textarea
                id="description"
                v-model="formData.description"
                placeholder="Optional description..."
                rows="3"
              ></textarea>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn-primary">{{ editingId ? 'Update' : 'Create' }}</button>
              <button type="button" @click="closeForm" class="btn-secondary">Cancel</button>
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
import { expenseService } from '../services/expenseService'

const categories = ref([])
const loading = ref(false)
const showForm = ref(false)
const editingId = ref(null)

const formData = ref({
  name: '',
  description: ''
})

const loadCategories = async () => {
  try {
    loading.value = true
    const response = await expenseService.getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('Failed to load categories:', error)
    alert('Failed to load categories')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formData.value = {
    name: '',
    description: ''
  }
  editingId.value = null
}

const showCreateForm = () => {
  resetForm()
  showForm.value = true
}

const editCategory = (category) => {
  formData.value = {
    name: category.name,
    description: category.description || ''
  }
  editingId.value = category.id
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
  resetForm()
}

const submitForm = async () => {
  try {
    if (editingId.value) {
      await expenseService.updateCategory(editingId.value, formData.value)
      alert('Category updated successfully')
    } else {
      await expenseService.createCategory(formData.value)
      alert('Category created successfully')
    }
    closeForm()
    loadCategories()
  } catch (error) {
    console.error('Failed to save category:', error)
    alert('Failed to save category')
  }
}

const deleteCategory = async (id) => {
  if (!confirm('Are you sure you want to delete this category?')) return

  try {
    await expenseService.deleteCategory(id)
    alert('Category deleted successfully')
    loadCategories()
  } catch (error) {
    console.error('Failed to delete category:', error)
    alert('Failed to delete category')
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

onMounted(() => {
  loadCategories()
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

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.category-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.category-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.card-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.btn-small {
  padding: 5px 10px;
  font-size: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
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

.category-description {
  margin: 10px 0;
  color: #666;
  font-size: 14px;
  min-height: 40px;
}

.created-date {
  display: block;
  color: #999;
  font-size: 12px;
  margin-top: 10px;
}

.empty-state,
.loading {
  text-align: center;
  padding: 40px 20px;
  background: white;
  border-radius: 8px;
}

.empty-state p,
.loading {
  color: #999;
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
  border-radius: 8px;
  padding: 30px;
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

.btn-close:hover {
  color: #333;
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
.form-group textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.btn-primary,
.btn-secondary {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}
</style>
