<template>
  <div class="search-page">
    <div class="container">
      <div class="search-layout">
        <!-- Filters Sidebar -->
        <aside class="filters">
          <h3>Filters</h3>
          
          <div class="filter-group">
            <label>Price Range</label>
            <div class="price-inputs">
              <input 
                v-model.number="localFilters.minPrice" 
                type="number" 
                placeholder="Min"
                @input="updateFilters"
              />
              <span>to</span>
              <input 
                v-model.number="localFilters.maxPrice" 
                type="number" 
                placeholder="Max"
                @input="updateFilters"
              />
            </div>
          </div>

          <div class="filter-group">
            <label>Bedrooms</label>
            <input 
              v-model.number="localFilters.minBedrooms" 
              type="number" 
              min="0"
              placeholder="Min bedrooms"
              @input="updateFilters"
            />
          </div>

          <div class="filter-group">
            <label>Bathrooms</label>
            <input 
              v-model.number="localFilters.minBathrooms" 
              type="number" 
              min="0"
              step="0.5"
              placeholder="Min bathrooms"
              @input="updateFilters"
            />
          </div>

          <div class="filter-group">
            <label>Property Type</label>
            <select v-model="localFilters.propertyType" @change="updateFilters">
              <option value="">All Types</option>
              <option value="single-family">Single Family</option>
              <option value="condo">Condo</option>
              <option value="townhouse">Townhouse</option>
              <option value="multi-family">Multi-Family</option>
              <option value="land">Land</option>
            </select>
          </div>

          <button class="btn btn-primary" @click="clearAllFilters">
            Clear Filters
          </button>
        </aside>

        <!-- Results -->
        <main class="results">
          <div class="results-header">
            <h2>Search Results</h2>
            <p>{{ propertiesStore.filteredProperties.length }} properties found</p>
          </div>

          <div v-if="propertiesStore.loading" class="loading">
            Loading properties...
          </div>

          <div v-else-if="propertiesStore.error" class="error">
            {{ propertiesStore.error }}
          </div>

          <div v-else class="properties-grid">
            <p v-if="propertiesStore.filteredProperties.length === 0">
              No properties match your criteria. Try adjusting your filters.
            </p>
            <!-- Property cards will go here -->
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import type { PropertyFilters } from '@/types/property'

const route = useRoute()
const propertiesStore = usePropertiesStore()

const localFilters = ref<PropertyFilters>({
  minPrice: undefined,
  maxPrice: undefined,
  minBedrooms: undefined,
  minBathrooms: undefined,
  propertyType: undefined
})

const updateFilters = () => {
  propertiesStore.setFilters(localFilters.value)
}

const clearAllFilters = () => {
  localFilters.value = {
    minPrice: undefined,
    maxPrice: undefined,
    minBedrooms: undefined,
    minBathrooms: undefined,
    propertyType: undefined
  }
  propertiesStore.clearFilters()
}

onMounted(() => {
  propertiesStore.fetchProperties()
  
  // Handle search query from URL
  const searchQuery = route.query.q as string
  if (searchQuery) {
    // TODO: Add search query to filters
    console.log('Search query:', searchQuery)
  }
})
</script>

<style scoped>
.search-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: var(--spacing-xl);
  padding: var(--spacing-xl) 0;
}

.filters {
  background: var(--color-surface);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  height: fit-content;
  position: sticky;
  top: var(--spacing-lg);
}

.filters h3 {
  margin-bottom: var(--spacing-lg);
  font-size: var(--font-size-xl);
}

.filter-group {
  margin-bottom: var(--spacing-lg);
}

.filter-group label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.filter-group input,
.filter-group select {
  width: 100%;
  padding: var(--spacing-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
}

.price-inputs {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.price-inputs input {
  flex: 1;
}

.results-header {
  margin-bottom: var(--spacing-lg);
}

.results-header h2 {
  font-size: var(--font-size-2xl);
  margin-bottom: var(--spacing-xs);
}

.results-header p {
  color: var(--color-text-secondary);
}

.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.loading,
.error {
  padding: var(--spacing-lg);
  text-align: center;
}

.error {
  color: var(--color-error);
}

@media (max-width: 768px) {
  .search-layout {
    grid-template-columns: 1fr;
  }
  
  .filters {
    position: static;
  }
}
</style>