import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../pages/Home.vue';
import Modules from '../pages/Modules.vue';
import Login from '../pages/Login.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: 'Nexora Suite - Business Management Platform' }
  },
  {
    path: '/modules',
    name: 'Modules',
    component: Modules,
    meta: { title: 'Nexora Suite - Modules' }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: 'Nexora Suite - Login' }
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Nexora Suite';
  next();
});

export default router;
