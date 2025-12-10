<template>
  <div class="page">
    <div class="page-header">
      <router-link to="/" class="back-link">← Back</router-link>
      <h1>{{ isEdit ? 'Edit Job Ticket' : 'New Job Ticket' }}</h1>
    </div>

    <form @submit.prevent="submitForm" class="form">
      <div class="form-group">
        <label>Title *</label>
        <input v-model="form.title" type="text" required placeholder="e.g., AC Repair">
      </div>

      <div class="form-group">
        <label>Description</label>
        <textarea v-model="form.description" placeholder="Detailed description of the job"></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Customer Name *</label>
          <input v-model="form.customer_name" type="text" required placeholder="Customer name">
        </div>

        <div class="form-group">
          <label>Priority *</label>
          <select v-model="form.priority" required>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Customer Address</label>
          <input v-model="form.customer_address" type="text" placeholder="Customer address">
        </div>

        <div class="form-group">
          <label>Status</label>
          <select v-model="form.status">
            <option value="open">Open</option>
            <option value="assigned">Assigned</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label>Scheduled Date</label>
        <input v-model="form.scheduled_date" type="datetime-local">
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary">
          {{ isEdit ? 'Update Ticket' : 'Create Ticket' }}
        </button>
        <router-link to="/job-tickets" class="btn btn-secondary">Cancel</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import serviceService from '../services/serviceService';

export default {
  name: 'JobTicketForm',
  data() {
    return {
      form: {
        title: '',
        description: '',
        customer_name: '',
        customer_address: '',
        scheduled_date: '',
        priority: 'medium',
        status: 'open'
      },
      isEdit: false
    };
  },
  mounted() {
    if (this.$route.params.id) {
      this.isEdit = true;
      this.loadTicket();
    }
  },
  methods: {
    loadTicket() {
      serviceService.getJobTicket(this.$route.params.id)
        .then(response => {
          const data = response.data;
          this.form = {
            title: data.title,
            description: data.description,
            customer_name: data.customer_name,
            customer_address: data.customer_address,
            scheduled_date: data.scheduled_date,
            priority: data.priority,
            status: data.status
          };
        })
        .catch(error => console.error('Error loading ticket:', error));
    },
    submitForm() {
      if (this.isEdit) {
        serviceService.updateJobTicket(this.$route.params.id, this.form)
          .then(() => {
            alert('Job ticket updated successfully!');
            this.$router.push('/job-tickets');
          })
          .catch(error => {
            console.error('Error updating ticket:', error);
            alert('Error updating job ticket');
          });
      } else {
        serviceService.createJobTicket(this.form)
          .then(() => {
            alert('Job ticket created successfully!');
            this.$router.push('/job-tickets');
          })
          .catch(error => {
            console.error('Error creating ticket:', error);
            alert('Error creating job ticket');
          });
      }
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

.form {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

input, select, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
}

textarea {
  resize: vertical;
  min-height: 100px;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.btn {
  padding: 12px 24px;
  border-radius: 6px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
