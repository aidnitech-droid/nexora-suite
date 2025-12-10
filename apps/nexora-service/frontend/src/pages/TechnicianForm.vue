<template>
  <div class="page">
    <div class="page-header">
      <router-link to="/technicians" class="back-link">← Back</router-link>
      <h1>{{ isEdit ? 'Edit Technician' : 'New Technician' }}</h1>
    </div>

    <form @submit.prevent="submitForm" class="form">
      <div class="form-group">
        <label>Name *</label>
        <input v-model="form.name" type="text" required placeholder="Full name">
      </div>

      <div class="form-group">
        <label>Email</label>
        <input v-model="form.email" type="email" placeholder="email@example.com">
      </div>

      <div class="form-group">
        <label>Phone</label>
        <input v-model="form.phone" type="tel" placeholder="+1-555-0000">
      </div>

      <div class="form-group">
        <label>Skills</label>
        <textarea v-model="form.skills" placeholder="e.g., Electrical, Plumbing, HVAC (comma-separated)"></textarea>
      </div>

      <div v-if="isEdit" class="form-group">
        <label>
          <input v-model="form.active" type="checkbox">
          Active
        </label>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary">
          {{ isEdit ? 'Update Technician' : 'Create Technician' }}
        </button>
        <router-link to="/technicians" class="btn btn-secondary">Cancel</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import serviceService from '../services/serviceService';

export default {
  name: 'TechnicianForm',
  data() {
    return {
      form: {
        name: '',
        email: '',
        phone: '',
        skills: '',
        active: true
      },
      isEdit: false
    };
  },
  mounted() {
    if (this.$route.params.id) {
      this.isEdit = true;
      this.loadTechnician();
    }
  },
  methods: {
    loadTechnician() {
      serviceService.getTechnician(this.$route.params.id)
        .then(response => {
          const data = response.data;
          this.form = {
            name: data.name,
            email: data.email,
            phone: data.phone,
            skills: data.skills,
            active: data.active
          };
        })
        .catch(error => console.error('Error loading technician:', error));
    },
    submitForm() {
      if (this.isEdit) {
        serviceService.updateTechnician(this.$route.params.id, this.form)
          .then(() => {
            alert('Technician updated successfully!');
            this.$router.push('/technicians');
          })
          .catch(error => {
            console.error('Error updating technician:', error);
            alert('Error updating technician');
          });
      } else {
        serviceService.createTechnician(this.form)
          .then(() => {
            alert('Technician created successfully!');
            this.$router.push('/technicians');
          })
          .catch(error => {
            console.error('Error creating technician:', error);
            alert('Error creating technician');
          });
      }
    }
  }
};
</script>

<style scoped>
.page {
  padding: 20px;
  max-width: 600px;
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

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

label input[type="checkbox"] {
  width: auto;
  margin-right: 8px;
}

input, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
  box-sizing: border-box;
}

textarea {
  resize: vertical;
  min-height: 80px;
}

input:focus, textarea:focus {
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
</style>
