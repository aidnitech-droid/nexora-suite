import api from './api'

export const crmService = {
  // Leads
  getLeads: (page=1, perPage=20) => api.get('/leads', { params: { page, per_page: perPage } }),
  getLead: (id) => api.get(`/leads/${id}`),
  createLead: (data) => api.post('/leads', data),
  updateLead: (id, data) => api.put(`/leads/${id}`, data),
  deleteLead: (id) => api.delete(`/leads/${id}`),

  // Contacts
  getContacts: (page=1, perPage=20) => api.get('/contacts', { params: { page, per_page: perPage } }),
  getContact: (id) => api.get(`/contacts/${id}`),
  createContact: (data) => api.post('/contacts', data),
  updateContact: (id, data) => api.put(`/contacts/${id}`, data),
  deleteContact: (id) => api.delete(`/contacts/${id}`),

  // Deals
  getDeals: (page=1, perPage=20, params={}) => api.get('/deals', { params: { page, per_page: perPage, ...params } }),
  getDeal: (id) => api.get(`/deals/${id}`),
  createDeal: (data) => api.post('/deals', data),
  updateDeal: (id, data) => api.put(`/deals/${id}`, data),
  deleteDeal: (id) => api.delete(`/deals/${id}`),

  // Tasks
  getTasks: (page=1, perPage=20) => api.get('/tasks', { params: { page, per_page: perPage } }),
  getTask: (id) => api.get(`/tasks/${id}`),
  createTask: (data) => api.post('/tasks', data),
  updateTask: (id, data) => api.put(`/tasks/${id}`, data),
  deleteTask: (id) => api.delete(`/tasks/${id}`),

  // Analytics
  getAnalytics: () => api.get('/crm/analytics')
}
