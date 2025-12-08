import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Dashboard from '../pages/Dashboard.vue'
import Catalog from '../pages/Catalog.vue'
import ProductDetail from '../pages/ProductDetail.vue'
import Checkout from '../pages/Checkout.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/commerce', name: 'Catalog', component: Catalog },
  { path: '/commerce/new', name: 'NewProduct', component: ProductDetail, meta: { requiresAuth: true } },
  { path: '/commerce/:id', name: 'ProductDetail', component: ProductDetail },
  { path: '/checkout', name: 'Checkout', component: Checkout }
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
