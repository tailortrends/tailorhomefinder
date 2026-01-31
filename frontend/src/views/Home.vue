<template>
  <div class="home">
    <section class="hero">
      <div class="container">
        <h1>Find Your Dream Home</h1>
        <p class="subtitle">Search millions of homes for sale and for rent</p>
        
        <div class="search-bar">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Enter city, neighborhood, or ZIP code"
            @keyup.enter="handleSearch"
          />
          <button class="btn btn-primary" @click="handleSearch">
            Search
          </button>
        </div>
      </div>
    </section>

    <section class="featured-properties container">
      <h2>Featured Properties</h2>
      <div v-if="propertiesStore.loading">Loading...</div>
      <div v-else-if="propertiesStore.error" class="error">
        {{ propertiesStore.error }}
      </div>
      <div v-else class="properties-grid">
        <p v-if="propertiesStore.properties.length === 0">
          No properties available yet.
        </p>
        <!-- Property cards will go here -->
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'

const router = useRouter()
const propertiesStore = usePropertiesStore()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ 
      name: 'search', 
      query: { q: searchQuery.value } 
    })
  }
}

onMounted(() => {
  propertiesStore.fetchProperties()
})
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: white;
  padding: 4rem 0;
  text-align: center;
}

.hero h1 {
  font-size: var(--font-size-3xl);
  margin-bottom: var(--spacing-md);
}

.subtitle {
  font-size: var(--font-size-lg);
  margin-bottom: var(--spacing-xl);
  opacity: 0.9;
}

.search-bar {
  display: flex;
  gap: var(--spacing-sm);
  max-width: 600px;
  margin: 0 auto;
}

.search-bar input {
  flex: 1;
  padding: var(--spacing-md);
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
}

.featured-properties {
  padding: var(--spacing-xl) 0;
}

.featured-properties h2 {
  font-size: var(--font-size-2xl);
  margin-bottom: var(--spacing-lg);
}

.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.error {
  color: var(--color-error);
  padding: var(--spacing-md);
}
</style>