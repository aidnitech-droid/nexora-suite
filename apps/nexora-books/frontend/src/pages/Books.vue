<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="books-header">
        <h1>Books Management</h1>
        <button @click="showCreateForm = true" class="btn-add">+ Add Book</button>
      </div>

      <div v-if="showCreateForm" class="modal">
        <div class="modal-content">
          <h2>Add New Book</h2>
          <form @submit.prevent="handleCreateBook">
            <input v-model="newBook.title" placeholder="Title" required />
            <input v-model="newBook.author" placeholder="Author" required />
            <input v-model="newBook.isbn" placeholder="ISBN" required />
            <input v-model="newBook.price" type="number" placeholder="Price" />
            <input v-model="newBook.stock" type="number" placeholder="Stock" />
            <input v-model="newBook.category" placeholder="Category" />
            <textarea v-model="newBook.description" placeholder="Description"></textarea>
            <div class="form-actions">
              <button type="submit" class="btn-save">Save</button>
              <button type="button" @click="showCreateForm = false" class="btn-cancel">Cancel</button>
            </div>
          </form>
        </div>
      </div>

      <div class="books-list">
        <div v-for="book in books" :key="book.id" class="book-card">
          <h3>{{ book.title }}</h3>
          <p><strong>Author:</strong> {{ book.author }}</p>
          <p><strong>ISBN:</strong> {{ book.isbn }}</p>
          <p><strong>Price:</strong> ${{ book.price }}</p>
          <p><strong>Stock:</strong> {{ book.stock }}</p>
          <p v-if="book.category"><strong>Category:</strong> {{ book.category }}</p>
          <div class="card-actions">
            <router-link :to="`/books/${book.id}`" class="btn-view">View</router-link>
            <button @click="handleDeleteBook(book.id)" class="btn-delete">Delete</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { bookService } from '../services/bookService'

const books = ref([])
const showCreateForm = ref(false)
const newBook = ref({ title: '', author: '', isbn: '', price: 0, stock: 0, category: '', description: '' })

onMounted(async () => {
  await loadBooks()
})

const loadBooks = async () => {
  try {
    const response = await bookService.getBooks()
    books.value = response.data.books
  } catch (error) {
    console.error('Failed to load books:', error)
  }
}

const handleCreateBook = async () => {
  try {
    await bookService.createBook(newBook.value)
    showCreateForm.value = false
    newBook.value = { title: '', author: '', isbn: '', price: 0, stock: 0, category: '', description: '' }
    await loadBooks()
  } catch (error) {
    console.error('Failed to create book:', error)
  }
}

const handleDeleteBook = async (id) => {
  if (confirm('Are you sure you want to delete this book?')) {
    try {
      await bookService.deleteBook(id)
      await loadBooks()
    } catch (error) {
      console.error('Failed to delete book:', error)
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

.books-header {
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

.modal-content form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input, textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
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
  color: #333;
}

.books-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.book-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.book-card h3 {
  margin-top: 0;
  color: #333;
}

.book-card p {
  margin: 8px 0;
  color: #666;
  font-size: 14px;
}

.card-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.btn-view, .btn-delete {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
}

.btn-view {
  background: #667eea;
  color: white;
}

.btn-delete {
  background: #e74c3c;
  color: white;
}
</style>
