import Vue from 'vue';
import VueRouter from 'vue-router';
import Dashboard from '../pages/Dashboard.vue';
import RoutePlanner from '../pages/RoutePlanner.vue';
import RouteHistory from '../pages/RouteHistory.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'Nexora RouteIQ - Dashboard' }
  },
  {
    path: '/plan',
    name: 'RoutePlanner',
    component: RoutePlanner,
    meta: { title: 'Nexora RouteIQ - Plan Route' }
  },
  {
    path: '/history',
    name: 'RouteHistory',
    component: RouteHistory,
    meta: { title: 'Nexora RouteIQ - Route History' }
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Nexora RouteIQ';
  next();
});

export default router;
