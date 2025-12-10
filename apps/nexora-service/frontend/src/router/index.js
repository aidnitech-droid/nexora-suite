import Vue from 'vue';
import VueRouter from 'vue-router';
import Dashboard from '../pages/Dashboard.vue';
import Technicians from '../pages/Technicians.vue';
import JobTickets from '../pages/JobTickets.vue';
import JobTicketForm from '../pages/JobTicketForm.vue';
import JobTicketDetail from '../pages/JobTicketDetail.vue';
import TechnicianForm from '../pages/TechnicianForm.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'Nexora Service - Dashboard' }
  },
  {
    path: '/technicians',
    name: 'Technicians',
    component: Technicians,
    meta: { title: 'Nexora Service - Technicians' }
  },
  {
    path: '/technicians/new',
    name: 'NewTechnician',
    component: TechnicianForm,
    meta: { title: 'Nexora Service - New Technician' }
  },
  {
    path: '/technicians/:id/edit',
    name: 'EditTechnician',
    component: TechnicianForm,
    meta: { title: 'Nexora Service - Edit Technician' }
  },
  {
    path: '/job-tickets',
    name: 'JobTickets',
    component: JobTickets,
    meta: { title: 'Nexora Service - Job Tickets' }
  },
  {
    path: '/job-tickets/new',
    name: 'NewJobTicket',
    component: JobTicketForm,
    meta: { title: 'Nexora Service - New Job Ticket' }
  },
  {
    path: '/job-tickets/:id',
    name: 'JobTicketDetail',
    component: JobTicketDetail,
    meta: { title: 'Nexora Service - Job Ticket Detail' }
  },
  {
    path: '/job-tickets/:id/edit',
    name: 'EditJobTicket',
    component: JobTicketForm,
    meta: { title: 'Nexora Service - Edit Job Ticket' }
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Nexora Service';
  next();
});

export default router;
