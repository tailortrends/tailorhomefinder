<template>
  <header class="app-header">
    <div class="container header-content">
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
          <router-link :to="{ name: 'signup' }" class="btn btn-primary">
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
</script>

<style scoped>
.app-header {
  background: white;
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-md);
}

.logo {
  text-decoration: none;
  color: var(--color-primary);
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
  color: var(--color-text);
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover {
  color: var(--color-primary);
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
</style>