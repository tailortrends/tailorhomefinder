<template>
  <div class="search-page">
    <div class="container">
      <!-- Search Header -->
      <div class="search-header">
        <div class="search-info">
          <h1>Search Results</h1>
          <p class="result-count">{{ propertiesStore.filteredProperties.length }} properties found</p>
        </div>
        
        <!-- View Toggle -->
        <div class="view-toggle">
          <button 
            :class="['toggle-btn', { active: viewMode === 'grid' }]"
            @click="viewMode = 'grid'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect width="7" height="7" x="3" y="3" rx="1"/>
              <rect width="7" height="7" x="14" y="3" rx="1"/>
              <rect width="7" height="7" x="3" y="14" rx="1"/>
              <rect width="7" height="7" x="14" y="14" rx="1"/>
            </svg>
            Grid
          </button>
          <button 
            :class="['toggle-btn', { active: viewMode === 'map' }]"
            @click="viewMode = 'map'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/>
              <path d="M15 5.764v15"/>
              <path d="M9 3.236v15"/>
            </svg>
            Map
          </button>
        </div>
      </div>

      <div class="search-layout">
        <!-- Filters Sidebar -->
        <aside class="filters">
          <div class="filters-header">
            <h3>Filters</h3>
            <button 
              v-if="hasActiveFilters"
              class="clear-all-btn"
              @click="clearAllFilters"
            >
              Clear All
            </button>
          </div>
          
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
              <option value="House">Single Family</option>
              <option value="Condo">Condo</option>
              <option value="Townhouse">Townhouse</option>
              <option value="Land">Land</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Status</label>
            <select v-model="localFilters.status" @change="updateFilters">
              <option value="">All Status</option>
              <option value="Active">Active</option>
              <option value="Pending">Pending</option>
              <option value="Sold">Sold</option>
            </select>
          </div>

          <div class="filter-group">
            <label>City</label>
            <input 
              v-model="localFilters.city" 
              type="text"
              placeholder="Enter city name"
              @input="updateFilters"
            />
          </div>
        </aside>

        <!-- Results -->
        <main class="results">
          <!-- Loading State -->
          <div v-if="propertiesStore.loading" class="loading-state">
            <div class="spinner"></div>
            <p>Loading properties...</p>
          </div>

          <!-- Error State -->
          <div v-else-if="propertiesStore.error" class="error-state">
            <p>{{ propertiesStore.error }}</p>
            <button class="btn btn-primary" @click="propertiesStore.fetchProperties()">
              Try Again
            </button>
          </div>

          <!-- Map View -->
          <div v-else-if="viewMode === 'map'" class="map-view">
            <MapView
              :properties="propertiesStore.filteredProperties"
              :is-filtered="hasActiveFilters"
              @select="handlePropertySelect"
              @reset-filter="clearAllFilters"
            />
          </div>

          <!-- Grid View -->
          <div v-else-if="propertiesStore.filteredProperties.length > 0" class="properties-grid">
            <PropertyCard
              v-for="property in propertiesStore.filteredProperties"
              :key="property.id"
              :property="property"
              @select="handlePropertySelect"
            />
          </div>

          <!-- Empty State -->
          <div v-else class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.3-4.3"/>
            </svg>
            <h3>No properties match your criteria</h3>
            <p>Try adjusting your filters or search terms.</p>
            <button class="btn btn-primary" @click="clearAllFilters">
              Clear All Filters
            </button>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { usePropertiesStore } from '@/stores/properties';
import PropertyCard from '@/components/property/PropertyCard.vue';
import MapView from '@/components/property/MapView.vue';
import type { Property, PropertyFilters } from '@/types/property';

const route = useRoute();
const router = useRouter();
const propertiesStore = usePropertiesStore();

const viewMode = ref<'grid' | 'map'>('grid');

const localFilters = ref<PropertyFilters>({
  minPrice: undefined,
  maxPrice: undefined,
  minBedrooms: undefined,
  minBathrooms: undefined,
  propertyType: undefined,
  city: undefined,
  status: undefined
});

const hasActiveFilters = computed(() => {
  return Object.values(localFilters.value).some(value => 
    value !== undefined && value !== '' && value !== null
  );
});

const updateFilters = () => {
  propertiesStore.setFilters(localFilters.value);
};

const clearAllFilters = () => {
  localFilters.value = {
    minPrice: undefined,
    maxPrice: undefined,
    minBedrooms: undefined,
    minBathrooms: undefined,
    propertyType: undefined,
    city: undefined,
    status: undefined
  };
  propertiesStore.clearFilters();
};

const handlePropertySelect = (property: Property) => {
  router.push({
    name: 'property-detail',
    params: { id: property.id }
  });
};

onMounted(() => {
  propertiesStore.fetchProperties();
  
  // Handle search query from URL
  const searchQuery = route.query.q as string;
  if (searchQuery) {
    localFilters.value.city = searchQuery;
    updateFilters();
  }
});
</script>

<style scoped>
.search-page {
  padding: 2rem 0;
  min-height: 100vh;
}

.search-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--color-border);
}

.search-info h1 {
  font-family: var(--font-family-display);
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.25rem;
}

.result-count {
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);
}

.view-toggle {
  display: flex;
  gap: 0.5rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 0.25rem;
}

.toggle-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-sm);
  font-weight: 500;
  transition: all 0.2s ease;
}

.toggle-btn:hover {
  color: var(--color-text);
  background: rgba(212, 175, 55, 0.1);
}

.toggle-btn.active {
  background: var(--color-gold-500);
  color: #000;
}

.search-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 2rem;
}

.filters {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  height: fit-content;
  position: sticky;
  top: 2rem;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.filters h3 {
  font-family: var(--font-family-display);
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-text);
}

.clear-all-btn {
  background: none;
  border: none;
  color: var(--color-gold-500);
  font-size: var(--font-size-sm);
  font-weight: 600;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.clear-all-btn:hover {
  background: rgba(212, 175, 55, 0.1);
}

.filter-group {
  margin-bottom: 1.5rem;
}

.filter-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--color-text);
  font-size: var(--font-size-sm);
}

.filter-group input,
.filter-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  background: var(--color-background);
  color: var(--color-text);
  transition: border-color 0.2s ease;
}

.filter-group input:focus,
.filter-group select:focus {
  outline: none;
  border-color: var(--color-gold-500);
}

.price-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.price-inputs input {
  flex: 1;
}

.price-inputs span {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.results {
  min-height: 400px;
}

.map-view {
  width: 100%;
}

.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
}

.loading-state,
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loading-state {
  gap: 1rem;
}

.loading-state p {
  color: var(--color-text-secondary);
}

.error-state {
  color: var(--color-error);
}

.empty-state svg {
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  font-size: var(--font-size-2xl);
  color: var(--color-text);
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
}

@media (max-width: 1024px) {
  .search-layout {
    grid-template-columns: 1fr;
  }
  
  .filters {
    position: static;
  }
}

@media (max-width: 768px) {
  .search-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .view-toggle {
    width: 100%;
  }
  
  .toggle-btn {
    flex: 1;
    justify-content: center;
  }
  
  .properties-grid {
    grid-template-columns: 1fr;
  }
}
</style>