<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Nexora RouteIQ</h1>
      <p>Intelligent Route Planning for Sales Teams</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">🗺️</div>
        <div class="stat-info">
          <div class="stat-label">Total Routes Planned</div>
          <div class="stat-value">{{ stats.totalRoutes }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📏</div>
        <div class="stat-info">
          <div class="stat-label">Total Distance (km)</div>
          <div class="stat-value">{{ stats.totalDistance }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">⏱️</div>
        <div class="stat-info">
          <div class="stat-label">Total Time (hrs)</div>
          <div class="stat-value">{{ stats.totalTime }}</div>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>Quick Actions</h2>
      <div class="action-buttons">
        <router-link to="/plan" class="btn btn-primary">
          <span>+ Plan New Route</span>
        </router-link>
        <router-link to="/history" class="btn btn-secondary">
          <span>View Route History</span>
        </router-link>
      </div>
    </div>

    <div class="features">
      <h2>Features</h2>
      <div class="feature-grid">
        <div class="feature-card">
          <div class="feature-icon">🎯</div>
          <h3>Smart Route Optimization</h3>
          <p>Automatically optimize routes for shortest distance and time</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📍</div>
          <h3>Multiple Waypoints</h3>
          <p>Add multiple stops and waypoints to your route</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🚗</div>
          <h3>Travel Profiles</h3>
          <p>Choose driving, cycling, or walking profiles</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💾</div>
          <h3>Save Routes</h3>
          <p>Save and reuse frequently traveled routes</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {
        totalRoutes: 0,
        totalDistance: 0,
        totalTime: 0
      }
    };
  },
  mounted() {
    this.loadStats();
  },
  methods: {
    loadStats() {
      // Placeholder - would load from API
      this.stats = {
        totalRoutes: 12,
        totalDistance: 450,
        totalTime: 9
      };
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

.features {
  margin-bottom: 30px;
}

.features h2 {
  color: #333;
  margin: 0 0 15px 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.feature-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.feature-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.feature-card h3 {
  margin: 10px 0;
  color: #333;
  font-size: 16px;
}

.feature-card p {
  color: #666;
  font-size: 14px;
  margin: 0;
}
</style>
