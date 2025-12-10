import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:5050/api/routeiq';

export default {
  planRoute(routeData) {
    return axios.post(`${API_URL}/plan`, routeData);
  },

  healthCheck() {
    return axios.get(`${API_URL}/health`);
  },

  getSavedRoutes() {
    return axios.get(`${API_URL}/routes`);
  },

  saveRoute(routeData) {
    return axios.post(`${API_URL}/routes`, routeData);
  },

  deleteRoute(routeId) {
    return axios.delete(`${API_URL}/routes/${routeId}`);
  }
};
