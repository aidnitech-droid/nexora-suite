import api from './api'

const inventoryService = {
  // Warehouses
  getWarehouses() {
    return api.get('/warehouses')
  },

  createWarehouse(data) {
    return api.post('/warehouses', data)
  },

  updateWarehouse(id, data) {
    return api.put(`/warehouses/${id}`, data)
  },

  // Items
  getItems(page = 1, perPage = 10, filters = {}) {
    return api.get('/items', {
      params: {
        page,
        per_page: perPage,
        ...filters
      }
    })
  },

  getItem(id) {
    return api.get(`/items/${id}`)
  },

  createItem(data) {
    return api.post('/items', data)
  },

  updateItem(id, data) {
    return api.put(`/items/${id}`, data)
  },

  // Stock Batches
  getBatches(filters = {}) {
    return api.get('/batches', { params: filters })
  },

  createBatch(data) {
    return api.post('/batches', data)
  },

  // Purchase Orders
  getPurchaseOrders(page = 1, perPage = 10, filters = {}) {
    return api.get('/purchase-orders', {
      params: {
        page,
        per_page: perPage,
        ...filters
      }
    })
  },

  createPurchaseOrder(data) {
    return api.post('/purchase-orders', data)
  },

  receivePurchaseOrder(id) {
    return api.put(`/purchase-orders/${id}/receive`)
  },

  // Sale Orders
  getSaleOrders(page = 1, perPage = 10, filters = {}) {
    return api.get('/sale-orders', {
      params: {
        page,
        per_page: perPage,
        ...filters
      }
    })
  },

  createSaleOrder(data) {
    return api.post('/sale-orders', data)
  },

  fulfillSaleOrder(id) {
    return api.put(`/sale-orders/${id}/fulfill`)
  },

  // Alerts
  getAlerts(filters = {}) {
    return api.get('/alerts', { params: filters })
  },

  createAlert(data) {
    return api.post('/alerts', data)
  },

  resolveAlert(id) {
    return api.put(`/alerts/${id}/resolve`)
  },

  // Analytics
  getAnalyticsSummary() {
    return api.get('/analytics/summary')
  },

  getStockValueByCategory() {
    return api.get('/analytics/stock-value')
  },

  getWarehouseCapacity() {
    return api.get('/analytics/warehouse-capacity')
  },

  getInventoryMovement() {
    return api.get('/analytics/movement')
  }
}

export { inventoryService }
