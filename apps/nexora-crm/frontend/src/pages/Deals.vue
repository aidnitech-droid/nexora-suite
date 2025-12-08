<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>Deals</h1>
        <button @click="showCreate=true" class="btn-primary">+ New Deal</button>
      </div>

      <div v-if="loading" class="loading">Loading...</div>

      <div v-else class="deals-list">
        <div v-for="d in deals" :key="d.id" class="deal-card">
          <h3>{{ d.title }}</h3>
          <p>Amount: ${{ formatPrice(d.amount) }} • Stage: {{ d.stage }}</p>
        </div>
      </div>

      <div v-if="showCreate" class="modal" @click.self="showCreate=false">
        <div class="modal-content">
          <h3>Create Deal</h3>
          <form @submit.prevent="createDeal">
            <input v-model="form.title" placeholder="Title" required />
            <input v-model.number="form.amount" placeholder="Amount" type="number" />
            <select v-model="form.stage">
              <option value="prospect">Prospect</option>
              <option value="qualified">Qualified</option>
              <option value="proposal">Proposal</option>
              <option value="closed">Closed</option>
            </select>
            <div class="form-actions">
              <button type="submit" class="btn-primary">Create</button>
              <button type="button" @click="showCreate=false" class="btn-secondary">Cancel</button>
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
import { crmService } from '../services/crmService'

const deals = ref([])
const loading = ref(false)
const showCreate = ref(false)
const form = ref({ title:'', amount:0, stage:'prospect' })

const load = async () => {
  loading.value = true
  try {
    const res = await crmService.getDeals()
    deals.value = res.data.deals
  } catch (err) { console.error(err) }
  finally { loading.value = false }
}

const createDeal = async () => {
  try {
    await crmService.createDeal(form.value)
    showCreate.value = false
    form.value = { title:'', amount:0, stage:'prospect' }
    await load()
  } catch (err) { console.error(err); alert('Failed to create deal') }
}

const formatPrice = (v) => parseFloat(v).toFixed(2)

onMounted(() => load())
</script>

<style scoped>
.container{display:flex;height:100vh}
.main-content{flex:1;padding:20px}
.deal-card{background:white;padding:12px;border-radius:8px;margin-bottom:10px}
</style>
