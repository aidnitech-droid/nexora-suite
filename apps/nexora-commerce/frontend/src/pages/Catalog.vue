<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>🛍️ Catalog</h1>
        <router-link to="/commerce/new" class="btn-primary">+ New Product</router-link>
      </div>

      <div class="filters">
        <input v-model="filters.search" placeholder="Search products..." @input="loadProducts" />
        <select v-model="filters.category" @change="loadProducts">
          <option value="">All Categories</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>

      <div v-if="loading" class="loading">Loading...</div>

      <div v-else class="grid">
        <div v-for="p in products" :key="p.id" class="card">
          <h3>{{ p.name }}</h3>
          <p class="sku">{{ p.sku }}</p>
          <p class="price">${{ formatPrice(p.price) }}</p>
          <p class="stock">Stock: {{ p.quantity }}</p>
          <div class="actions">
            <router-link :to="`/commerce/${p.id}`" class="btn-view">View</router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { commerceService } from '../services/commerceService'

const loading = ref(false)
const products = ref([])
const categories = ref([])
const filters = ref({ search: '', category: '' })

const loadProducts = async () => {
  try {
    loading.value = true
    const res = await commerceService.getProducts(1, 50, { category: filters.value.category })
    products.value = res.data.items
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const res = await commerceService.getCategories()
    categories.value = res.data
  } catch (err) {
    console.error(err)
  }
}

const formatPrice = (v) => parseFloat(v).toFixed(2)

onMounted(() => {
  loadCategories()
  loadProducts()
})
</script>

<style scoped>
.container { display:flex; height:100vh; }
.main-content { flex:1; padding:20px; overflow:auto }
.page-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:20px }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:16px }
.card { background:white; padding:16px; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,.08) }
.sku { font-family:monospace; color:#666 }
.price { color:#27ae60; font-weight:700 }
.btn-view { background:#3498db; color:white; padding:6px 10px; border-radius:6px; text-decoration:none }
</style>
