<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="header">
        <h1>Items Management</h1>
        <button @click="showCreateForm = true" class="btn-add">+ Add Item</button>
      </div>

      <div v-if="showCreateForm" class="modal">
        <div class="modal-content">
          <h2>Add New Item</h2>
          <form @submit.prevent="handleCreateItem">
            <input v-model="newItem.title" placeholder="Title" required />
            <textarea v-model="newItem.description" placeholder="Description"></textarea>
            <div class="form-actions">
              <button type="submit" class="btn-save">Save</button>
              <button type="button" @click="showCreateForm = false" class="btn-cancel">Cancel</button>
            </div>
          </form>
        </div>
      </div>

      <div class="items-list">
        <div v-for="item in items" :key="item.id" class="item-card">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <button @click="handleDeleteItem(item.id)" class="btn-delete">Delete</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { itemService } from '../services/itemService'

const items = ref([])
const showCreateForm = ref(false)
const newItem = ref({ title: '', description: '' })

onMounted(loadItems)

async function loadItems() {
  try {
    const response = await itemService.getItems()
    items.value = response.data.items
  } catch (error) {
    console.error('Failed to load items:', error)
  }
}

async function handleCreateItem() {
  try {
    await itemService.createItem(newItem.value)
    showCreateForm.value = false
    newItem.value = { title: '', description: '' }
    await loadItems()
  } catch (error) {
    console.error('Failed to create item:', error)
  }
}

async function handleDeleteItem(id) {
  if (confirm('Delete this item?')) {
    try {
      await itemService.deleteItem(id)
      await loadItems()
    } catch (error) {
      console.error('Failed to delete item:', error)
    }
  }
}
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

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.btn-add {
  padding: 10px 20px;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
}

input, textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.form-actions {
  display: flex;
  gap: 10px;
}

.btn-save, .btn-cancel {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-save {
  background: #667eea;
  color: white;
}

.btn-cancel {
  background: #ddd;
}

.items-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.item-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.item-card h3 {
  margin-top: 0;
}

.btn-delete {
  width: 100%;
  padding: 8px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}
</style>
