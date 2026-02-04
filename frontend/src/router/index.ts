import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Favorites from '@/views/Favorites.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('@/views/Search.vue')
    },
    {
      path: '/property/:id',
      name: 'property-detail',
      component: () => import('@/views/PropertyDetail.vue')
    },
    {
      path: '/auth/login',
      name: 'login',
      component: () => import('@/views/Auth/Login.vue')
    },
    {
      path: '/auth/signup',
      name: 'signup',
      component: () => import('@/views/Auth/Signup.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/views/Admin.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: Favorites,
      meta: {
        title: 'My Favorites'
        // Optionally add: requiresAuth: true (if you implement auth)
      }
    }
  ]
})

// Navigation guard
router.beforeEach((to) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login' }
  }
})

export default router