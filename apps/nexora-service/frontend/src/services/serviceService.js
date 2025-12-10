import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000/api';

export default {
  // Technician endpoints
  listTechnicians(page = 1, perPage = 10) {
    return axios.get(`${API_URL}/technicians`, { params: { page, per_page: perPage } });
  },

  getTechnician(id) {
    return axios.get(`${API_URL}/technicians/${id}`);
  },

  createTechnician(data) {
    return axios.post(`${API_URL}/technicians`, data);
  },

  updateTechnician(id, data) {
    return axios.put(`${API_URL}/technicians/${id}`, data);
  },

  deleteTechnician(id) {
    return axios.delete(`${API_URL}/technicians/${id}`);
  },

  // Job Ticket endpoints
  listJobTickets(page = 1, perPage = 10, filters = {}) {
    return axios.get(`${API_URL}/job-tickets`, { params: { page, per_page: perPage, ...filters } });
  },

  getJobTicket(id) {
    return axios.get(`${API_URL}/job-tickets/${id}`);
  },

  createJobTicket(data) {
    return axios.post(`${API_URL}/job-tickets`, data);
  },

  updateJobTicket(id, data) {
    return axios.put(`${API_URL}/job-tickets/${id}`, data);
  },

  deleteJobTicket(id) {
    return axios.delete(`${API_URL}/job-tickets/${id}`);
  },

  assignTechnician(jobId, technicianId) {
    return axios.put(`${API_URL}/job-tickets/${jobId}`, { technician_id: technicianId });
  },

  updateJobStatus(jobId, status) {
    return axios.put(`${API_URL}/job-tickets/${jobId}`, { status });
  }
};
