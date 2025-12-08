import api from './api'

const expenseService = {
  // Expenses
  getExpenses(page = 1, perPage = 10, filters = {}) {
    return api.get('/expenses', {
      params: {
        page,
        per_page: perPage,
        ...filters
      }
    })
  },

  getExpense(id) {
    return api.get(`/expenses/${id}`)
  },

  createExpense(data) {
    return api.post('/expenses', data)
  },

  updateExpense(id, data) {
    return api.put(`/expenses/${id}`, data)
  },

  deleteExpense(id) {
    return api.delete(`/expenses/${id}`)
  },

  // Categories
  getCategories() {
    return api.get('/categories')
  },

  createCategory(data) {
    return api.post('/categories', data)
  },

  updateCategory(id, data) {
    return api.put(`/categories/${id}`, data)
  },

  deleteCategory(id) {
    return api.delete(`/categories/${id}`)
  },

  // Attachments
  uploadAttachment(expenseId, formData) {
    return api.post(`/expenses/${expenseId}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  downloadAttachment(attachmentId) {
    return api.get(`/attachments/${attachmentId}`, {
      responseType: 'blob'
    })
  },

  deleteAttachment(attachmentId) {
    return api.delete(`/attachments/${attachmentId}`)
  }
}

export { expenseService }
