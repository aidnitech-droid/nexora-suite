<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div v-if="loading" class="loading">Loading product...</div>
      <div v-else class="product">
        <h1>{{ product.name }}</h1>
        <p class="sku">{{ product.sku }}</p>
        <p class="price">${{ formatPrice(product.price) }}</p>
        <p class="description">{{ product.description }}</p>
        <p class="stock">Available: {{ product.quantity }}</p>

        <div class="buy">
          <input type="number" v-model.number="qty" min="1" :max="product.quantity" />
          <button @click="addToCart" class="btn-primary">Add to Cart</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import { commerceService } from '../services/commerceService'

const route = useRoute()
const router = useRouter()
const product = ref(null)
const loading = ref(false)
const qty = ref(1)

const loadProduct = async () => {
  loading.value = true
  try {
    const res = await commerceService.getProduct(route.params.id)
    product.value = res.data
  } catch (err) {
    console.error(err)
    alert('Product not found')
    router.push('/commerce')
  } finally {
    loading.value = false
  }
}

const formatPrice = (v) => parseFloat(v).toFixed(2)

const addToCart = () => {
  const cart = JSON.parse(localStorage.getItem('cart') || '[]')
  cart.push({ product_id: product.value.id, quantity: qty.value })
  localStorage.setItem('cart', JSON.stringify(cart))
  alert('Added to cart')
}

onMounted(() => loadProduct())
</script>

<style scoped>
.container { display:flex; height:100vh }
.main-content { flex:1; padding:20px; overflow:auto }
.product { background:white; padding:20px; border-radius:8px }
.sku { font-family:monospace; color:#666 }
.price { color:#27ae60; font-weight:700 }
.buy { margin-top:20px; display:flex; gap:10px; align-items:center }
</style>
