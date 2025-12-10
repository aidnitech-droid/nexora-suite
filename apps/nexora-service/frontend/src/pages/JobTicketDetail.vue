<template>
  <div class="page">
    <div class="page-header">
      <router-link to="/job-tickets" class="back-link">← Back</router-link>
      <h1>Job Ticket Details</h1>
    </div>

    <div v-if="loading" class="loading">Loading ticket details...</div>
    <div v-else-if="ticket" class="detail-container">
      <div class="detail-card">
        <div class="detail-header">
          <h2>{{ ticket.title }}</h2>
          <span :class="`status status-${ticket.status}`">{{ ticket.status }}</span>
        </div>

        <div class="detail-grid">
          <div class="detail-row">
            <label>Customer Name:</label>
            <p>{{ ticket.customer_name || 'N/A' }}</p>
          </div>

          <div class="detail-row">
            <label>Customer Address:</label>
            <p>{{ ticket.customer_address || 'N/A' }}</p>
          </div>

          <div class="detail-row">
            <label>Priority:</label>
            <p>
              <span :class="`priority priority-${ticket.priority}`">
                {{ ticket.priority }}
              </span>
            </p>
          </div>

          <div class="detail-row">
            <label>Scheduled Date:</label>
            <p>{{ formatDate(ticket.scheduled_date) }}</p>
          </div>

          <div class="detail-row full-width">
            <label>Description:</label>
            <p>{{ ticket.description || 'No description provided' }}</p>
          </div>

          <div class="detail-row full-width">
            <label>Created:</label>
            <p>{{ formatDate(ticket.created_at) }}</p>
          </div>
        </div>

        <div class="action-buttons">
          <router-link :to="`/job-tickets/${ticket.id}/edit`" class="btn btn-primary">
            Edit Ticket
          </router-link>
          <button @click="deleteTicket" class="btn btn-danger">Delete</button>
          <router-link to="/job-tickets" class="btn btn-secondary">Back to List</router-link>
        </div>
      </div>
    </div>
    <div v-else class="error">
      <p>Ticket not found</p>
      <router-link to="/job-tickets" class="link">Back to list</router-link>
    </div>
  </div>
</template>

<script>
import serviceService from '../services/serviceService';

export default {
  name: 'JobTicketDetail',
  data() {
    return {
      ticket: null,
      loading: false
    };
  },
  mounted() {
    this.loadTicket();
  },
  methods: {
    loadTicket() {
      this.loading = true;
      serviceService.getJobTicket(this.$route.params.id)
        .then(response => {
          this.ticket = response.data;
        })
        .catch(error => {
          console.error('Error loading ticket:', error);
          this.ticket = null;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    deleteTicket() {
      if (confirm('Are you sure you want to delete this ticket?')) {
        serviceService.deleteJobTicket(this.$route.params.id)
          .then(() => {
            alert('Ticket deleted successfully!');
            this.$router.push('/job-tickets');
          })
          .catch(error => {
            console.error('Error deleting ticket:', error);
            alert('Error deleting ticket');
          });
      }
    },
    formatDate(date) {
      if (!date) return 'N/A';
      return new Date(date).toLocaleString();
    }
  }
};
</script>

<style scoped>
.page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
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

.loading, .error {
  text-align: center;
  padding: 40px;
  color: #999;
}

.detail-card {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #eee;
}

.detail-header h2 {
  margin: 0;
  color: #333;
}

.status {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
}

.status-open { background: #e7f3ff; color: #004085; }
.status-assigned { background: #fff3cd; color: #856404; }
.status-in_progress { background: #d1ecf1; color: #0c5460; }
.status-completed { background: #d4edda; color: #155724; }

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.detail-row {
  display: flex;
  flex-direction: column;
}

.detail-row.full-width {
  grid-column: 1 / -1;
}

.detail-row label {
  font-weight: 600;
  color: #666;
  margin-bottom: 8px;
}

.detail-row p {
  margin: 0;
  color: #333;
}

.priority {
  padding: 3px 8px;
  border-radius: 3px;
  font-size: 12px;
}

.priority-high { background: #fff3cd; color: #856404; }
.priority-medium { background: #d1ecf1; color: #0c5460; }
.priority-low { background: #d4edda; color: #155724; }

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 2px solid #eee;
}

.btn {
  padding: 12px 24px;
  border-radius: 6px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

.link {
  color: #007bff;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}
</style>
