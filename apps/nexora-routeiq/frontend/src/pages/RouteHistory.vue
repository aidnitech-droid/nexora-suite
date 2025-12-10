<template>
  <div class="page">
    <div class="page-header">
      <router-link to="/" class="back-link">← Back</router-link>
      <h1>Route History</h1>
    </div>

    <div v-if="loading" class="loading">Loading route history...</div>
    <div v-else-if="routes.length" class="routes-table">
      <table>
        <thead>
          <tr>
            <th>Route Name</th>
            <th>Profile</th>
            <th>Distance (km)</th>
            <th>Duration (min)</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="route in routes" :key="route.id">
            <td>{{ route.name }}</td>
            <td>
              <span class="profile-badge" :class="`profile-${route.profile}`">
                {{ route.profile }}
              </span>
            </td>
            <td>{{ route.distance_km.toFixed(2) }}</td>
            <td>{{ Math.round(route.duration_min) }}</td>
            <td>{{ formatDate(route.created_at) }}</td>
            <td>
              <button @click="deleteRoute(route.id)" class="link link-danger">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="empty-state">
      <p>No saved routes yet. <router-link to="/plan">Plan a route</router-link></p>
    </div>
  </div>
</template>

<script>
import routeService from '../services/routeService';

export default {
  name: 'RouteHistory',
  data() {
    return {
      routes: [],
      loading: false
    };
  },
  mounted() {
    this.loadRoutes();
  },
  methods: {
    loadRoutes() {
      this.loading = true;
      routeService.getSavedRoutes()
        .then(response => {
          this.routes = response.data.items || [];
        })
        .catch(error => {
          console.error('Error loading routes:', error);
          this.routes = [];
        })
        .finally(() => {
          this.loading = false;
        });
    },
    deleteRoute(id) {
      if (confirm('Are you sure you want to delete this route?')) {
        routeService.deleteRoute(id)
          .then(() => {
            this.loadRoutes();
          })
          .catch(error => console.error('Error deleting route:', error));
      }
    },
    formatDate(date) {
      if (!date) return 'N/A';
      return new Date(date).toLocaleDateString();
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

.loading {
  text-align: center;
  padding: 40px;
  color: #999;
}

.routes-table {
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

.profile-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.profile-driving-car {
  background: #d1ecf1;
  color: #0c5460;
}

.profile-cycling-regular {
  background: #d4edda;
  color: #155724;
}

.profile-foot-walking {
  background: #fff3cd;
  color: #856404;
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
  background: white;
  border-radius: 8px;
}
</style>
