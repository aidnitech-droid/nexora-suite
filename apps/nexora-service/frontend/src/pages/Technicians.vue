<template>
  <div class="page">
    <div class="page-header">
      <router-link to="/" class="back-link">← Back</router-link>
      <h1>Technicians</h1>
    </div>

    <div class="actions">
      <router-link to="/technicians/new" class="btn btn-primary">+ Add Technician</router-link>
    </div>

    <div v-if="loading" class="loading">Loading technicians...</div>
    <div v-else-if="technicians.length" class="tech-grid">
      <div v-for="tech in technicians" :key="tech.id" class="tech-card">
        <div class="tech-header">
          <h3>{{ tech.name }}</h3>
          <span v-if="tech.active" class="badge badge-active">Active</span>
          <span v-else class="badge badge-inactive">Inactive</span>
        </div>
        <div class="tech-details">
          <p v-if="tech.email"><strong>Email:</strong> {{ tech.email }}</p>
          <p v-if="tech.phone"><strong>Phone:</strong> {{ tech.phone }}</p>
          <p v-if="tech.skills"><strong>Skills:</strong> {{ tech.skills }}</p>
        </div>
        <div class="tech-actions">
          <router-link :to="`/technicians/${tech.id}/edit`" class="link">Edit</router-link>
          <button @click="deleteTechnician(tech.id)" class="link link-danger">Delete</button>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <p>No technicians yet. <router-link to="/technicians/new">Add one</router-link></p>
    </div>
  </div>
</template>

<script>
import serviceService from '../services/serviceService';

export default {
  name: 'Technicians',
  data() {
    return {
      technicians: [],
      loading: false
    };
  },
  mounted() {
    this.loadTechnicians();
  },
  methods: {
    loadTechnicians() {
      this.loading = true;
      serviceService.listTechnicians(1, 50)
        .then(response => {
          this.technicians = response.data.items || [];
        })
        .catch(error => {
          console.error('Error loading technicians:', error);
          this.technicians = [];
        })
        .finally(() => {
          this.loading = false;
        });
    },
    deleteTechnician(id) {
      if (confirm('Are you sure you want to delete this technician?')) {
        serviceService.deleteTechnician(id)
          .then(() => {
            this.loadTechnicians();
          })
          .catch(error => console.error('Error deleting technician:', error));
      }
    }
  }
};
</script>

<style scoped>
.page {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.back-link {
  display: inline-block;
  color: #007bff;
  text-decoration: none;
  margin-bottom: 10px;
}

.page-header h1 {
  font-size: 28px;
  color: #333;
  margin: 0;
}

.actions {
  margin-bottom: 30px;
}

.btn {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  display: inline-block;
}

.btn:hover {
  background: #0056b3;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #999;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.tech-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.tech-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 10px;
}

.tech-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.badge-active {
  background: #d4edda;
  color: #155724;
}

.badge-inactive {
  background: #f8d7da;
  color: #721c24;
}

.tech-details {
  flex: 1;
}

.tech-details p {
  margin: 8px 0;
  color: #666;
  font-size: 14px;
}

.tech-actions {
  display: flex;
  gap: 10px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.link {
  color: #007bff;
  text-decoration: none;
  cursor: pointer;
  border: none;
  background: none;
  padding: 0;
  font-size: 14px;
}

.link:hover {
  text-decoration: underline;
}

.link-danger {
  color: #dc3545;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}
</style>
