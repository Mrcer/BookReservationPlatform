import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      redirect: '/home',
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/views/AdminView.vue'),
    },
    {
      path: '/detail/:id',
      name: 'detail',
      component: () => import('@/views/DetailView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
      children: [
        {
          path: 'general',
          name: 'general',
          component: () => import('@/components/Profile/General.vue'),
        },
        {
          path: 'reservations',
          name:'reservations',
          component: () => import('@/components/Profile/Reservations.vue'),
        },
        {
          path: 'borrowed',
          name: 'borrowed',
          component: () => import('@/components/Profile/Borrowed.vue'),
        }
      ],
      // TODO: 如果还没登陆，则跳转到登录页面
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('@/views/SearchView.vue'),
    },
    {
      path: '/reserve',
      name: 'reserve',
      component: () => import('@/views/ReserveView.vue'),
    },
  ],
})

export default router
