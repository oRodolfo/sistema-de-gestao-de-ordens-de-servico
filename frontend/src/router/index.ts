import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/cadastro',
      name: 'Cadastro',
      component: () => import('@/views/CadastroView.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue')
    },
    {
      path: '/abrir-os',
      name: 'abrir-os',
      component: () => import('@/views/AbrirOsView.vue')
    },
    {
      path: '/dashboard-gerente',
      name: 'dashboard-gerente',
      component: () => import('@/views/DashboardGerenteView.vue')
    }
  ],
})

export default router
