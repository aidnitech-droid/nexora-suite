import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Dashboard from '../pages/Dashboard.vue'
import Inventory from '../pages/Inventory.vue'
import ItemForm from '../pages/ItemForm.vue'
import PurchaseOrders from '../pages/PurchaseOrders.vue'
import SaleOrders from '../pages/SaleOrders.vue'
import Alerts from '../pages/Alerts.vue'
import Warehouses from '../pages/Warehouses.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/inventory', name: 'Inventory', component: Inventory, meta: { requiresAuth: true } },
  { path: '/inventory/new', name: 'NewItem', component: ItemForm, meta: { requiresAuth: true } },
  { path: '/inventory/:id/edit', name: 'EditItem', component: ItemForm, meta: { requiresAuth: true } },
  { path: '/purchase-orders', name: 'PurchaseOrders', component: PurchaseOrders, meta: { requiresAuth: true } },
  { path: '/sale-orders', name: 'SaleOrders', component: SaleOrders, meta: { requiresAuth: true } },
  { path: '/alerts', name: 'Alerts', component: Alerts, meta: { requiresAuth: true } },
  { path: '/warehouses', name: 'Warehouses', component: Warehouses, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
