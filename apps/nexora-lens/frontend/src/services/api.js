import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000/api';

export default {
  // Generic CRUD operations
  list(resource, page = 1, perPage = 10, filters = {}) {
    return axios.get(`${API_URL}/${resource}`, { params: { page, per_page: perPage, ...filters } });
  },

  get(resource, id) {
    return axios.get(`${API_URL}/${resource}/${id}`);
  },

  create(resource, data) {
    return axios.post(`${API_URL}/${resource}`, data);
  },

  update(resource, id, data) {
    return axios.put(`${API_URL}/${resource}/${id}`, data);
  },

  delete(resource, id) {
    return axios.delete(`${API_URL}/${resource}/${id}`);
  },

  // Health check
  health() {
    return axios.get(`${API_URL}/health`);
  }
};
