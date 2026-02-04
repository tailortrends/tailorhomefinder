<template>
  <header class="app-header">
    <div class="container header-content">
      <nav class="navigation">
      <RouterLink to="/" class="nav-link">Home</RouterLink>
      <RouterLink to="/search" class="nav-link">Search</RouterLink>
      
      <!-- Add Favorites Link -->
      <RouterLink to="/favorites" class="nav-link favorites-link">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
        Favorites
        <span v-if="favoritesStore.favoritesCount > 0" class="favorites-badge">
          {{ favoritesStore.favoritesCount }}
        </span>
      </RouterLink>
      
      <router-link :to="{ name: 'home' }" class="logo">
        <h1>Tailor Home Finder</h1>
      </router-link>

      <nav class="nav-menu">
        <router-link :to="{ name: 'search' }" class="nav-link">
          Search
        </router-link>
        
        <template v-if="authStore.isAuthenticated">
          <router-link :to="{ name: 'dashboard' }" class="nav-link">
            Dashboard
          </router-link>
          <button @click="handleLogout" class="nav-link btn-link">
            Sign Out
          </button>
        </template>
        
        <template v-else>
          <router-link :to="{ name: 'login' }" class="nav-link">
            Sign In
          </router-link>
          <router-link :to="{ name: 'signup' }" class="btn btn-primary hover:scale-105 transition-transform">
            Sign Up
          </router-link>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useFavoritesStore } from '@/stores/favorites'


const favoritesStore = useFavoritesStore()

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push({ name: 'home' })
  } catch (error) {
    console.error('Logout error:', error)
  }
}

// Load favorites on mount
onMounted(() => {
  favoritesStore.loadFavorites()
})
</script>

<style scoped>
.app-header {
  background: rgba(12, 12, 12, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-md);
}

.logo {
  text-decoration: none;
  color: var(--color-gold-400);
}

.logo h1 {
  font-size: var(--font-size-xl);
  font-weight: 700;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.nav-link {
  text-decoration: none;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover {
  color: var(--color-gold-400);
}

.btn-link {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  font-size: var(--font-size-base);
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .nav-menu {
    width: 100%;
    justify-content: center;
  }
}
.favorites-link {
  @apply relative flex items-center gap-2;
}

.favorites-badge {
  @apply absolute -top-1 -right-1;
  @apply bg-error text-white;
  @apply text-xs font-bold;
  @apply w-5 h-5 rounded-full;
  @apply flex items-center justify-center;
  @apply shadow-md;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

/* Optional: Active state styling */
.nav-link.router-link-active.favorites-link {
  @apply text-error;
}
</style>