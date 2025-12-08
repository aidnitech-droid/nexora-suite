<template>
  <div class="container">
    <Sidebar />
    <main class="main-content">
      <div class="page-header">
        <h1>Tasks</h1>
        <button @click="showCreate=true" class="btn-primary">+ New Task</button>
      </div>

      <div v-if="loading" class="loading">Loading...</div>

      <div v-else class="tasks-list">
        <div v-for="t in tasks" :key="t.id" class="task-card">
          <h3>{{ t.title }}</h3>
          <p>Status: {{ t.status }} • Due: {{ t.due_date ? new Date(t.due_date).toLocaleDateString() : '—' }}</p>
        </div>
      </div>

      <div v-if="showCreate" class="modal" @click.self="showCreate=false">
        <div class="modal-content">
          <h3>Create Task</h3>
          <form @submit.prevent="createTask">
            <input v-model="form.title" placeholder="Title" required />
            <textarea v-model="form.description" placeholder="Description"></textarea>
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

const tasks = ref([])
const loading = ref(false)
const showCreate = ref(false)
const form = ref({ title:'', description:'' })

const load = async () => {
  loading.value = true
  try {
    const res = await crmService.getTasks()
    tasks.value = res.data.tasks
  } catch (err) { console.error(err) }
  finally { loading.value = false }
}

const createTask = async () => {
  try {
    await crmService.createTask(form.value)
    showCreate.value = false
    form.value = { title:'', description:'' }
    await load()
  } catch (err) { console.error(err); alert('Failed to create task') }
}

onMounted(() => load())
</script>

<style scoped>
.container{display:flex;height:100vh}
.main-content{flex:1;padding:20px}
.task-card{background:white;padding:12px;border-radius:8px;margin-bottom:10px}
</style>
