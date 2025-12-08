<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>Checkout</h1>
      </div>

      <div class="checkout-card">
        <div v-if="cart.length === 0">Your cart is empty.</div>

        <div v-else>
          <div v-for="(item, idx) in detailedCart" :key="idx" class="cart-item">
            <div>{{ item.product.name }} x {{ item.quantity }}</div>
            <div>${{ formatPrice(item.line_total) }}</div>
          </div>

          <div class="total">Total: ${{ formatPrice(total) }}</div>

          <form @submit.prevent="doCheckout">
            <input v-model="form.customer_name" placeholder="Full name" required />
            <input v-model="form.customer_email" placeholder="Email" type="email" required />
            <button type="submit" class="btn-primary">Place Order</button>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { commerceService } from '../services/commerceService'

const cart = ref([])
const detailedCart = ref([])
const total = ref(0)
const form = ref({ customer_name: '', customer_email: '' })
const loading = ref(false)

const loadCart = async () => {
  cart.value = JSON.parse(localStorage.getItem('cart') || '[]')
  if (cart.value.length === 0) return
  try {
    const ids = cart.value.map(c => c.product_id)
    const products = await Promise.all(ids.map(id => commerceService.getProduct(id).then(r=>r.data)))
    detailedCart.value = cart.value.map(c => {
      const prod = products.find(p => p.id === c.product_id)
      const line = parseFloat(prod.price) * c.quantity
      return { product: prod, quantity: c.quantity, line_total: line }
    })
    total.value = detailedCart.value.reduce((s, i) => s + i.line_total, 0)
  } catch (err) {
    console.error(err)
  }
}

const formatPrice = (v) => parseFloat(v).toFixed(2)

const doCheckout = async () => {
  try {
    loading.value = true
    const payload = {
      customer_name: form.value.customer_name,
      customer_email: form.value.customer_email,
      items: cart.value
    }
    const res = await commerceService.checkout(payload)
    alert('Order placed: ' + res.data.order_number)
    localStorage.removeItem('cart')
    detailedCart.value = []
    cart.value = []
    total.value = 0
  } catch (err) {
    console.error(err)
    alert('Failed to place order')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadCart()
})
</script>

<style scoped>
.container { display:flex; height:100vh }
.main-content { flex:1; padding:20px; overflow:auto }
.checkout-card { background:white; padding:20px; border-radius:8px }
.cart-item { display:flex; justify-content:space-between; padding:8px 0 }
.total { font-weight:700; margin-top:10px }
</style>
