<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <router-link to="/books" class="btn-back">← Back to Books</router-link>
      <div v-if="book" class="book-detail">
        <h1>{{ book.title }}</h1>
        <div class="detail-content">
          <div class="detail-info">
            <p><strong>Author:</strong> {{ book.author }}</p>
            <p><strong>ISBN:</strong> {{ book.isbn }}</p>
            <p><strong>Category:</strong> {{ book.category || 'N/A' }}</p>
            <p><strong>Price:</strong> ${{ book.price }}</p>
            <p><strong>Stock:</strong> {{ book.stock }}</p>
            <p><strong>Created:</strong> {{ new Date(book.created_at).toLocaleDateString() }}</p>
          </div>
          <div class="detail-description">
            <h3>Description</h3>
            <p>{{ book.description || 'No description available' }}</p>
          </div>
        </div>
        <div class="detail-actions">
          <button @click="showEditForm = true" class="btn-edit">Edit</button>
          <button @click="handleDelete" class="btn-delete">Delete</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import { bookService } from '../services/bookService'

const route = useRoute()
const router = useRouter()
const book = ref(null)
const showEditForm = ref(false)

onMounted(async () => {
  try {
    const response = await bookService.getBook(route.params.id)
    book.value = response.data
  } catch (error) {
    console.error('Failed to load book:', error)
  }
})

const handleDelete = async () => {
  if (confirm('Are you sure you want to delete this book?')) {
    try {
      await bookService.deleteBook(route.params.id)
      router.push('/books')
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

.btn-back {
  display: inline-block;
  margin-bottom: 20px;
  color: #667eea;
  text-decoration: none;
  cursor: pointer;
}

.book-detail {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.book-detail h1 {
  margin-top: 0;
  color: #333;
}

.detail-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin: 20px 0;
}

.detail-info p, .detail-description p {
  margin: 10px 0;
  color: #666;
  line-height: 1.6;
}

.detail-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-edit, .btn-delete {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  color: white;
}

.btn-edit {
  background: #667eea;
}

.btn-delete {
  background: #e74c3c;
}
</style>
