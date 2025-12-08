<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>Leads</h1>
        <button @click="showCreate = true" class="btn-primary">+ New Lead</button>
      </div>

      <div v-if="loading" class="loading">Loading...</div>

      <div v-else class="leads-list">
        <div v-for="lead in leads" :key="lead.id" class="lead-card">
          <h3>{{ lead.name }}</h3>
          <p>{{ lead.email }} • {{ lead.phone }}</p>
          <div class="actions">
            <button @click="viewLead(lead.id)" class="btn-small">View</button>
          </div>
        </div>
      </div>

      <div v-if="showCreate" class="modal" @click.self="showCreate=false">
        <div class="modal-content">
          <h3>Create Lead</h3>
          <form @submit.prevent="createLead">
            <input v-model="form.name" placeholder="Name" required />
            <input v-model="form.email" placeholder="Email" />
            <input v-model="form.phone" placeholder="Phone" />
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
import { useRouter } from 'vue-router'

const router = useRouter()
const leads = ref([])
const loading = ref(false)
const showCreate = ref(false)
const form = ref({ name:'', email:'', phone:'' })

const load = async () => {
  loading.value = true
  try {
    const res = await crmService.getLeads()
    leads.value = res.data.leads
  } catch (err) { console.error(err) }
  finally { loading.value = false }
}

const createLead = async () => {
  try {
    await crmService.createLead(form.value)
    showCreate.value = false
    form.value = { name:'', email:'', phone:'' }
    await load()
  } catch (err) { console.error(err); alert('Failed to create lead') }
}

const viewLead = (id) => {
  router.push(`/crm/leads/${id}`)
}

onMounted(() => load())
</script>

<style scoped>
.container{display:flex;height:100vh}
.main-content{flex:1;padding:20px}
.lead-card{background:white;padding:12px;border-radius:8px;margin-bottom:10px}
</style>
