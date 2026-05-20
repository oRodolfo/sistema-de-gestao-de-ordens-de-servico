import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
    },
    {
      path: '/abrir-os',
      name: 'abrir-os',
      component: () => import('@/views/AbrirOsView.vue'),
    },
    {
      path: '/dashboard-gerente',
      component: () => import('@/views/DashboardGerenteView.vue'),
      children: [
        {
          path: 'indicadores',
          component: () => import('@/views/IndicadoresView.vue'),
        },
        {
          path: 'funcionarios',
          component: () => import('@/views/FuncionariosView.vue'),
        },
        {
          path: 'ordens',
          component: () => import('@/views/OrdensView.vue'),
        },
      ],
    },
    {
      path: '/dashboard-gestor',
      component: () => import('@/views/DashboardGestorView.vue'),
      children: [
        {
          path: 'ordens',
          component: () => import('@/views/OrdensGestorView.vue'),
        },
        {
          path: 'indicadores',
          component: () => import('@/views/Indicadoresgestorview.vue'),
        },
      ],
    },
    {
      path: '/dashboard-tecnico',
      component: () => import('@/views/DashboardTecnicoView.vue'),
      children: [
        {
          path: 'ordens',
          component: () => import('@/views/OrdensTecnicoView.vue'),
        },
      ],
    },
  ],
})

export default router