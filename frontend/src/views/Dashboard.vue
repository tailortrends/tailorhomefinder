<template>
  <div class="dashboard">
    <div class="container">
      <header class="dashboard-header">
        <div>
          <h1>My Dashboard</h1>
          <p v-if="authStore.user">Welcome, {{ authStore.user.email }}</p>
        </div>
        <button class="btn" @click="handleLogout">Sign Out</button>
      </header>

      <div class="dashboard-content">
        <section class="stats-grid">
          <div class="stat-card">
            <h3>Saved Properties</h3>
            <p class="stat-number">0</p>
          </div>
          <div class="stat-card">
            <h3>Recent Searches</h3>
            <p class="stat-number">0</p>
          </div>
          <div class="stat-card">
            <h3>Notifications</h3>
            <p class="stat-number">0</p>
          </div>
        </section>

        <section class="recent-activity">
          <h2>Recent Activity</h2>
          <p class="empty-state">No recent activity yet. Start searching for properties!</p>
          <router-link :to="{ name: 'search' }" class="btn btn-primary">
            Browse Properties
          </router-link>
        </section>
      </div>
    </div>
  </div>
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
.dashboard {
  min-height: 100vh;
  background: var(--color-surface);
  padding: var(--spacing-xl) 0;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border);
}

.dashboard-header h1 {
  font-size: var(--font-size-2xl);
  margin-bottom: var(--spacing-xs);
}

.dashboard-header p {
  color: var(--color-text-secondary);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.stat-card {
  background: white;
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.stat-card h3 {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-sm);
}

.stat-number {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-primary);
}

.recent-activity {
  background: white;
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.recent-activity h2 {
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-lg);
}

.empty-state {
  color: var(--color-text-secondary);
  text-align: center;
  padding: var(--spacing-xl) 0;
  margin-bottom: var(--spacing-lg);
}
</style>