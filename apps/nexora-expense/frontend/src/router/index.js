import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Dashboard from '../pages/Dashboard.vue'
import Items from '../pages/Items.vue'
import Expenses from '../pages/Expenses.vue'
import ExpenseForm from '../pages/ExpenseForm.vue'
import ExpenseDetail from '../pages/ExpenseDetail.vue'
import Categories from '../pages/Categories.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/items', name: 'Items', component: Items, meta: { requiresAuth: true } },
  { path: '/expenses', name: 'Expenses', component: Expenses, meta: { requiresAuth: true } },
  { path: '/expenses/new', name: 'CreateExpense', component: ExpenseForm, meta: { requiresAuth: true } },
  { path: '/expenses/:id', name: 'ExpenseDetail', component: ExpenseDetail, meta: { requiresAuth: true } },
  { path: '/expenses/:id/edit', name: 'EditExpense', component: ExpenseForm, meta: { requiresAuth: true } },
  { path: '/categories', name: 'Categories', component: Categories, meta: { requiresAuth: true } }
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
