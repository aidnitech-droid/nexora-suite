<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>Contacts</h1>
      </div>

      <div v-if="loading" class="loading">Loading...</div>

      <div v-else class="contacts-list">
        <div v-for="c in contacts" :key="c.id" class="contact-card">
          <h3>{{ c.name }}</h3>
          <p>{{ c.email }} • {{ c.phone }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { crmService } from '../services/crmService'

const contacts = ref([])
const loading = ref(false)

const load = async () => {
  loading.value = true
  try {
    const res = await crmService.getContacts()
    contacts.value = res.data.contacts
  } catch (err) { console.error(err) }
  finally { loading.value = false }
}

onMounted(() => load())
</script>

<style scoped>
.container{display:flex;height:100vh}
.main-content{flex:1;padding:20px}
.contact-card{background:white;padding:12px;border-radius:8px;margin-bottom:10px}
</style>
