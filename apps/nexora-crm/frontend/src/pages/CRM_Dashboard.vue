<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="dashboard-header">
        <h1>CRM Dashboard</h1>
        <button @click="refresh" class="btn-refresh">Refresh</button>
      </div>

      <div v-if="loading" class="loading">Loading...</div>

      <div v-else class="stats-grid">
        <div class="stat-card"> <h3>Leads</h3> <p class="stat-value">{{ analytics.total_leads }}</p> </div>
        <div class="stat-card"> <h3>Contacts</h3> <p class="stat-value">{{ analytics.total_contacts }}</p> </div>
        <div class="stat-card"> <h3>Deals</h3> <p class="stat-value">{{ analytics.total_deals }}</p> </div>
        <div class="stat-card"> <h3>Open Deals</h3> <p class="stat-value">{{ analytics.open_deals }}</p> </div>
      </div>

      <div class="pipeline">
        <h2>Pipeline</h2>
        <div v-for="p in analytics.pipeline" :key="p.stage" class="pipeline-row">
          <div class="stage">{{ p.stage }}</div>
          <div class="count">{{ p.count }}</div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { crmService } from '../services/crmService'

const loading = ref(false)
const analytics = ref({ total_leads:0, total_contacts:0, total_deals:0, open_deals:0, closed_deals:0, pipeline:[] })

const load = async () => {
  loading.value = true
  try {
    const res = await crmService.getAnalytics()
    analytics.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const refresh = () => load()

onMounted(() => load())
</script>

<style scoped>
.container { display:flex; height:100vh }
.main-content { flex:1; padding:20px; overflow:auto }
.stats-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:12px; margin-bottom:20px }
.stat-card { background:white; padding:16px; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,.06) }
.stat-value { font-size:28px; font-weight:700 }
.pipeline { background:white; padding:16px; border-radius:8px }
.pipeline-row { display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #f1f1f1 }
</style>
