<template>
  <div class="page">
    <div class="page-header">
      <router-link to="/" class="back-link">← Back</router-link>
      <h1>Plan a Route</h1>
    </div>

    <form @submit.prevent="planRoute" class="route-form">
      <div class="form-section">
        <h2>Route Details</h2>

        <div class="form-group">
          <label>Travel Profile *</label>
          <select v-model="form.profile" required>
            <option value="driving-car">🚗 Driving</option>
            <option value="cycling-regular">🚴 Cycling</option>
            <option value="foot-walking">🚶 Walking</option>
          </select>
        </div>

        <div class="coordinates-section">
          <h3>Origin Location</h3>
          <div class="coord-inputs">
            <div class="form-group">
              <label>Latitude *</label>
              <input v-model.number="form.origin[0]" type="number" step="0.0001" placeholder="e.g., 40.7128" required>
            </div>
            <div class="form-group">
              <label>Longitude *</label>
              <input v-model.number="form.origin[1]" type="number" step="0.0001" placeholder="e.g., -74.0060" required>
            </div>
          </div>
        </div>

        <div class="coordinates-section">
          <h3>Destination Location</h3>
          <div class="coord-inputs">
            <div class="form-group">
              <label>Latitude *</label>
              <input v-model.number="form.destination[0]" type="number" step="0.0001" placeholder="e.g., 40.7580" required>
            </div>
            <div class="form-group">
              <label>Longitude *</label>
              <input v-model.number="form.destination[1]" type="number" step="0.0001" placeholder="e.g., -73.9855" required>
            </div>
          </div>
        </div>

        <div class="waypoints-section">
          <h3>Waypoints (Optional)</h3>
          <p class="hint">Add intermediate stops along the route</p>
          <div v-for="(waypoint, index) in form.waypoints" :key="index" class="waypoint">
            <div class="coord-inputs">
              <div class="form-group">
                <label>Stop {{ index + 1 }} Latitude</label>
                <input v-model.number="waypoint[0]" type="number" step="0.0001" placeholder="Latitude">
              </div>
              <div class="form-group">
                <label>Stop {{ index + 1 }} Longitude</label>
                <input v-model.number="waypoint[1]" type="number" step="0.0001" placeholder="Longitude">
              </div>
            </div>
            <button @click="removeWaypoint(index)" type="button" class="btn-remove">Remove</button>
          </div>
          <button @click="addWaypoint" type="button" class="btn btn-secondary">+ Add Waypoint</button>
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="planning">
          {{ planning ? 'Planning Route...' : 'Plan Route' }}
        </button>
        <router-link to="/" class="btn btn-outline">Cancel</router-link>
      </div>
    </form>

    <div v-if="routeResult" class="route-result">
      <h2>Route Details</h2>
      <div class="result-grid">
        <div class="result-card">
          <div class="result-label">Total Distance</div>
          <div class="result-value">{{ routeResult.distance_km.toFixed(2) }} km</div>
        </div>
        <div class="result-card">
          <div class="result-label">Estimated Duration</div>
          <div class="result-value">{{ Math.round(routeResult.duration_min) }} min</div>
        </div>
      </div>

      <div class="route-summary">
        <h3>Route Summary</h3>
        <div class="summary-text">
          <p>Your {{ form.profile }} route from origin to destination{{ form.waypoints.length > 0 ? ' via ' + form.waypoints.length + ' waypoint(s)' : '' }} has been planned.</p>
          <p>You can save this route for future reference.</p>
        </div>
        <button @click="saveRoute" class="btn btn-primary">💾 Save Route</button>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
import routeService from '../services/routeService';

export default {
  name: 'RoutePlanner',
  data() {
    return {
      form: {
        origin: [40.7128, -74.0060],
        destination: [40.7580, -73.9855],
        waypoints: [],
        profile: 'driving-car'
      },
      routeResult: null,
      planning: false,
      error: null
    };
  },
  methods: {
    planRoute() {
      this.planning = true;
      this.error = null;

      const payload = {
        origin: this.form.origin,
        destination: this.form.destination,
        profile: this.form.profile
      };

      if (this.form.waypoints.length > 0) {
        payload.waypoints = this.form.waypoints.filter(w => w[0] && w[1]);
      }

      routeService.planRoute(payload)
        .then(response => {
          this.routeResult = response.data;
        })
        .catch(error => {
          console.error('Error planning route:', error);
          this.error = error.response?.data?.error || 'Failed to plan route';
          this.routeResult = null;
        })
        .finally(() => {
          this.planning = false;
        });
    },
    addWaypoint() {
      this.form.waypoints.push([0, 0]);
    },
    removeWaypoint(index) {
      this.form.waypoints.splice(index, 1);
    },
    saveRoute() {
      const routeData = {
        name: `Route - ${new Date().toLocaleDateString()}`,
        profile: this.form.profile,
        origin: this.form.origin,
        destination: this.form.destination,
        waypoints: this.form.waypoints,
        distance_km: this.routeResult.distance_km,
        duration_min: this.routeResult.duration_min
      };

      routeService.saveRoute(routeData)
        .then(() => {
          alert('Route saved successfully!');
          this.$router.push('/history');
        })
        .catch(error => {
          console.error('Error saving route:', error);
          alert('Failed to save route');
        });
    }
  }
};
</script>

<style scoped>
.page {
  padding: 20px;
  max-width: 900px;
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

.route-form {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 30px;
}

.form-section h2 {
  font-size: 20px;
  color: #333;
  margin: 0 0 20px 0;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

input, select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

input:focus, select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
}

.coordinates-section {
  margin: 20px 0;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 6px;
}

.coordinates-section h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #333;
}

.coord-inputs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.waypoints-section {
  margin: 25px 0;
  padding: 15px;
  background: #f0f8ff;
  border-radius: 6px;
}

.waypoints-section h3 {
  margin: 0 0 5px 0;
  font-size: 16px;
  color: #333;
}

.hint {
  margin: 0 0 15px 0;
  font-size: 13px;
  color: #666;
}

.waypoint {
  margin-bottom: 15px;
  padding: 15px;
  background: white;
  border-radius: 4px;
  border: 1px solid #ddd;
  position: relative;
}

.btn-remove {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.btn-remove:hover {
  background: #c82333;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 25px;
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

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
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

.route-result {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.route-result h2 {
  margin: 0 0 20px 0;
  color: #333;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 25px;
}

.result-card {
  padding: 15px;
  background: #f0f8ff;
  border-radius: 6px;
  text-align: center;
}

.result-label {
  font-size: 13px;
  color: #666;
  text-transform: uppercase;
  margin-bottom: 5px;
}

.result-value {
  font-size: 28px;
  font-weight: bold;
  color: #007bff;
}

.route-summary {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 6px;
}

.route-summary h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.summary-text p {
  margin: 8px 0;
  color: #666;
  line-height: 1.6;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 6px;
  margin-top: 20px;
  border: 1px solid #f5c6cb;
}

@media (max-width: 600px) {
  .coord-inputs {
    grid-template-columns: 1fr;
  }

  .result-grid {
    grid-template-columns: 1fr;
  }
}
</style>
