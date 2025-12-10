<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Nexora Service Management</h1>
      <p>Field Service & Technician Management System</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">👨‍🔧</div>
        <div class="stat-info">
          <div class="stat-label">Total Technicians</div>
          <div class="stat-value">{{ stats.totalTechnicians }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-info">
          <div class="stat-label">Open Jobs</div>
          <div class="stat-value">{{ stats.openJobs }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">⚡</div>
        <div class="stat-info">
          <div class="stat-label">In Progress</div>
          <div class="stat-value">{{ stats.inProgressJobs }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <div class="stat-label">Completed</div>
          <div class="stat-value">{{ stats.completedJobs }}</div>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>Quick Actions</h2>
      <div class="action-buttons">
        <router-link to="/job-tickets/new" class="btn btn-primary">
          <span>+ New Job Ticket</span>
        </router-link>
        <router-link to="/technicians/new" class="btn btn-secondary">
          <span>+ Add Technician</span>
        </router-link>
        <router-link to="/job-tickets" class="btn btn-outline">
          <span>View All Jobs</span>
        </router-link>
        <router-link to="/technicians" class="btn btn-outline">
          <span>View Technicians</span>
        </router-link>
      </div>
    </div>

    <div class="recent-jobs">
      <h2>Recent Job Tickets</h2>
      <div v-if="recentJobs.length" class="jobs-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Customer</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="job in recentJobs" :key="job.id">
              <td>{{ job.id }}</td>
              <td>{{ job.title }}</td>
              <td>{{ job.customer_name || 'N/A' }}</td>
              <td>
                <span :class="`priority priority-${job.priority}`">
                  {{ job.priority }}
                </span>
              </td>
              <td>
                <span :class="`status status-${job.status}`">
                  {{ job.status }}
                </span>
              </td>
              <td>{{ formatDate(job.created_at) }}</td>
              <td>
                <router-link :to="`/job-tickets/${job.id}`" class="link">View</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="empty-state">
        <p>No jobs yet. <router-link to="/job-tickets/new">Create one now</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import serviceService from '../services/serviceService';

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {
        totalTechnicians: 0,
        openJobs: 0,
        inProgressJobs: 0,
        completedJobs: 0
      },
      recentJobs: []
    };
  },
  mounted() {
    this.loadStats();
    this.loadRecentJobs();
  },
  methods: {
    loadStats() {
      serviceService.listTechnicians(1, 1)
        .then(response => {
          this.stats.totalTechnicians = response.data.total || 0;
        })
        .catch(error => console.error('Error loading technicians:', error));

      serviceService.listJobTickets(1, 100)
        .then(response => {
          const jobs = response.data.items || [];
          this.stats.openJobs = jobs.filter(j => j.status === 'open').length;
          this.stats.inProgressJobs = jobs.filter(j => j.status === 'in_progress').length;
          this.stats.completedJobs = jobs.filter(j => j.status === 'completed').length;
        })
        .catch(error => console.error('Error loading job stats:', error));
    },
    loadRecentJobs() {
      serviceService.listJobTickets(1, 5)
        .then(response => {
          this.recentJobs = response.data.items || [];
        })
        .catch(error => console.error('Error loading recent jobs:', error));
    },
    formatDate(date) {
      if (!date) return 'N/A';
      return new Date(date).toLocaleDateString();
    }
  }
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.dashboard-header {
  margin-bottom: 30px;
}

.dashboard-header h1 {
  font-size: 28px;
  color: #333;
  margin: 0 0 5px 0;
}

.dashboard-header p {
  color: #666;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-icon {
  font-size: 32px;
}

.stat-label {
  font-size: 12px;
  color: #999;
  text-transform: uppercase;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.quick-actions {
  margin-bottom: 30px;
}

.quick-actions h2 {
  margin: 0 0 15px 0;
  color: #333;
}

.action-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 20px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
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

.btn-outline {
  border: 2px solid #ddd;
  color: #333;
}

.btn-outline:hover {
  border-color: #007bff;
  color: #007bff;
}

.recent-jobs h2 {
  color: #333;
  margin: 0 0 15px 0;
}

.jobs-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: #f8f9fa;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #ddd;
}

td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.priority {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.priority-high {
  background: #fff3cd;
  color: #856404;
}

.priority-medium {
  background: #d1ecf1;
  color: #0c5460;
}

.priority-low {
  background: #d4edda;
  color: #155724;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.status-open {
  background: #e7f3ff;
  color: #004085;
}

.status-assigned {
  background: #fff3cd;
  color: #856404;
}

.status-in_progress {
  background: #d1ecf1;
  color: #0c5460;
}

.status-completed {
  background: #d4edda;
  color: #155724;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.link {
  color: #007bff;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}
</style>
