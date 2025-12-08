import api from './api'

export const authService = {
  login: (username, password) => api.post('/auth/login', { username, password }),
  register: (username, email, password) => api.post('/auth/register', { username, email, password })
}

export const itemService = {
  getItems: (page = 1, perPage = 10) => api.get('/items', { params: { page, per_page: perPage } }),
  getItem: (id) => api.get(`/items/${id}`),
  createItem: (data) => api.post('/items', data),
  updateItem: (id, data) => api.put(`/items/${id}`, data),
  deleteItem: (id) => api.delete(`/items/${id}`)
}
