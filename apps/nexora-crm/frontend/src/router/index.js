import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Dashboard from '../pages/Dashboard.vue'
import CRM_Dashboard from '../pages/CRM_Dashboard.vue'
import Leads from '../pages/Leads.vue'
import Contacts from '../pages/Contacts.vue'
import Deals from '../pages/Deals.vue'
import Tasks from '../pages/Tasks.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/crm', name: 'CRM_Dashboard', component: CRM_Dashboard, meta: { requiresAuth: true } },
  { path: '/crm/leads', name: 'Leads', component: Leads, meta: { requiresAuth: true } },
  { path: '/crm/contacts', name: 'Contacts', component: Contacts, meta: { requiresAuth: true } },
  { path: '/crm/deals', name: 'Deals', component: Deals, meta: { requiresAuth: true } },
  { path: '/crm/tasks', name: 'Tasks', component: Tasks, meta: { requiresAuth: true } }
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
