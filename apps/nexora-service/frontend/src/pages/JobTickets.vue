<template>
  <div class="page">
    <div class="page-header">
      <router-link to="/" class="back-link">← Back</router-link>
      <h1>Job Tickets</h1>
    </div>

    <div class="filter-section">
      <div class="filter-group">
        <label>Filter by Status:</label>
        <select v-model="selectedStatus" @change="loadJobTickets">
          <option value="">All Statuses</option>
          <option value="open">Open</option>
          <option value="assigned">Assigned</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Priority:</label>
        <select v-model="selectedPriority" @change="loadJobTickets">
          <option value="">All Priorities</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>
      <router-link to="/job-tickets/new" class="btn btn-primary">+ New Job Ticket</router-link>
    </div>

    <div v-if="loading" class="loading">Loading job tickets...</div>
    <div v-else-if="jobTickets.length" class="jobs-grid">
      <div v-for="ticket in jobTickets" :key="ticket.id" class="job-card">
        <div class="job-header">
          <h3>{{ ticket.title }}</h3>
          <span :class="`status status-${ticket.status}`">{{ ticket.status }}</span>
        </div>
        <div class="job-details">
          <p><strong>Customer:</strong> {{ ticket.customer_name || 'N/A' }}</p>
          <p><strong>Priority:</strong> 
            <span :class="`priority priority-${ticket.priority}`">{{ ticket.priority }}</span>
          </p>
          <p><strong>Description:</strong> {{ ticket.description || 'N/A' }}</p>
        </div>
        <div class="job-actions">
          <router-link :to="`/job-tickets/${ticket.id}`" class="link">View Details</router-link>
          <router-link :to="`/job-tickets/${ticket.id}/edit`" class="link">Edit</router-link>
          <button @click="deleteTicket(ticket.id)" class="link link-danger">Delete</button>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <p>No job tickets found. <router-link to="/job-tickets/new">Create one</router-link></p>
    </div>
  </div>
</template>

<script>
import serviceService from '../services/serviceService';

export default {
  name: 'JobTickets',
  data() {
    return {
      jobTickets: [],
      loading: false,
      selectedStatus: '',
      selectedPriority: ''
    };
  },
  mounted() {
    this.loadJobTickets();
  },
  methods: {
    loadJobTickets() {
      this.loading = true;
      const filters = {};
      if (this.selectedStatus) filters.status = this.selectedStatus;
      if (this.selectedPriority) filters.priority = this.selectedPriority;

      serviceService.listJobTickets(1, 50, filters)
        .then(response => {
          this.jobTickets = response.data.items || [];
        })
        .catch(error => {
          console.error('Error loading job tickets:', error);
          this.jobTickets = [];
        })
        .finally(() => {
          this.loading = false;
        });
    },
    deleteTicket(id) {
      if (confirm('Are you sure you want to delete this job ticket?')) {
        serviceService.deleteJobTicket(id)
          .then(() => {
            this.loadJobTickets();
          })
          .catch(error => console.error('Error deleting ticket:', error));
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

.back-link:hover {
  text-decoration: underline;
}

.page-header h1 {
  font-size: 28px;
  color: #333;
  margin: 0;
}

.filter-section {
  display: flex;
  gap: 15px;
  align-items: flex-end;
  margin-bottom: 30px;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.filter-group {
  flex: 1;
  min-width: 200px;
}

.filter-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
}

.filter-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.btn {
  padding: 10px 20px;
  border-radius: 6px;
  background: #007bff;
  color: white;
  text-decoration: none;
  font-weight: 500;
  border: none;
  cursor: pointer;
}

.btn:hover {
  background: #0056b3;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #999;
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.job-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 10px;
}

.job-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.status-open { background: #e7f3ff; color: #004085; }
.status-assigned { background: #fff3cd; color: #856404; }
.status-in_progress { background: #d1ecf1; color: #0c5460; }
.status-completed { background: #d4edda; color: #155724; }

.job-details {
  flex: 1;
}

.job-details p {
  margin: 8px 0;
  color: #666;
}

.priority {
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
}

.priority-high { background: #fff3cd; color: #856404; }
.priority-medium { background: #d1ecf1; color: #0c5460; }
.priority-low { background: #d4edda; color: #155724; }

.job-actions {
  display: flex;
  gap: 10px;
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
