import api from './api'

export const authService = {
  login: (username, password) => api.post('/auth/login', { username, password }),
  register: (username, email, password) => api.post('/auth/register', { username, email, password }),
  logout: () => localStorage.removeItem('token')
}

export const bookService = {
  getBooks: (page = 1, perPage = 10) => api.get('/books', { params: { page, per_page: perPage } }),
  getBook: (id) => api.get(`/books/${id}`),
  createBook: (data) => api.post('/books', data),
  updateBook: (id, data) => api.put(`/books/${id}`, data),
  deleteBook: (id) => api.delete(`/books/${id}`)
}
