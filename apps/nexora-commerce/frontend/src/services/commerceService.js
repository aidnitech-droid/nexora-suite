import api from './api'

export const commerceService = {
  // Categories
  getCategories: () => api.get('/categories'),
  createCategory: (data) => api.post('/categories', data),

  // Products
  getProducts: (page = 1, perPage = 20, params = {}) => api.get('/products', { params: { page, per_page: perPage, ...params } }),
  getProduct: (id) => api.get(`/products/${id}`),
  createProduct: (data) => api.post('/products', data),

  // Checkout
  checkout: (data) => api.post('/checkout', data),

  // Storefronts
  getStorefronts: () => api.get('/storefronts'),
  createStorefront: (data) => api.post('/storefronts', data),
  renderStorefront: (slug) => api.get(`/store/${slug}`)
}
