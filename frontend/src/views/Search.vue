<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import SearchFilters from '@/components/property/SearchFilters.vue'
import PropertyGrid from '@/components/property/PropertyGrid.vue'
import Pagination from '@/components/property/Pagination.vue'
import type { Property, PropertyFilters } from '@/types/property'

const router = useRouter()
const propertiesStore = usePropertiesStore()

// Sort options
const sortOptions = [
  { label: 'Newest', value: 'newest' },
  { label: 'Price: Low to High', value: 'price' },
  { label: 'Price: High to Low', value: 'price_desc' },
  { label: 'Square Feet', value: 'sqft' },
  { label: 'Bedrooms', value: 'beds' }
]

const selectedSort = ref(propertiesStore.sortBy)

// Load properties on mount
onMounted(async () => {
  if (propertiesStore.properties.length === 0) {
    await propertiesStore.fetchProperties()
  }
})

// Watch for sort changes
watch(selectedSort, (newSort) => {
  propertiesStore.setSortBy(newSort as any)
})

// Handle filter updates
function handleFiltersUpdate(newFilters: PropertyFilters) {
  propertiesStore.updateFilters(newFilters)
}

// Handle search
async function handleSearch() {
  const location = propertiesStore.filters.location
  
  // Check if location is a ZIP code (5 digits)
  if (location && /^\d{5}$/.test(location)) {
    await propertiesStore.fetchProperties(location)
  } else {
    // For now, just fetch all properties
    // In production, this would search by city/state
    await propertiesStore.fetchProperties()
  }
}

// Handle property click
function handlePropertyClick(property: Property) {
  router.push({
    name: 'property-detail',
    params: { id: property.property_id }
  })
}

// Handle page change
function handlePageChange(page: number) {
  propertiesStore.setPage(page)
  // Scroll to top of results
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
  <div class="search-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          Find Your Dream Home
        </h1>
        <p class="hero-subtitle">
          Search through thousands of luxury properties
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-8">
      <!-- Search Filters -->
      <SearchFilters
        :filters="propertiesStore.filters"
        @update:filters="handleFiltersUpdate"
        @search="handleSearch"
      />

      <!-- Results Header -->
      <div class="results-header">
        <div class="results-info">
          <h2 class="results-count">
            {{ propertiesStore.totalProperties }} 
            {{ propertiesStore.totalProperties === 1 ? 'Property' : 'Properties' }}
            {{ propertiesStore.hasFilters ? 'Match Your Search' : 'Available' }}
          </h2>
          
          <p v-if="propertiesStore.filters.location" class="results-location">
            in {{ propertiesStore.filters.location }}
          </p>
        </div>

        <!-- Sort Dropdown -->
        <div class="sort-control">
          <label class="sort-label">Sort by:</label>
          <select
            v-model="selectedSort"
            class="select select-bordered select-sm"
          >
            <option
              v-for="option in sortOptions"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>
        </div>
      </div>

      <!-- Property Grid -->
      <PropertyGrid
        :properties="propertiesStore.paginatedProperties"
        :loading="propertiesStore.loading"
        @property-click="handlePropertyClick"
      />

      <!-- Pagination -->
      <Pagination
        v-if="propertiesStore.totalPages > 1"
        :current-page="propertiesStore.currentPage"
        :total-pages="propertiesStore.totalPages"
        :total-items="propertiesStore.totalProperties"
        @page-change="handlePageChange"
      />

      <!-- Error State -->
      <div v-if="propertiesStore.error" class="alert alert-error mt-6">
        <svg
          class="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span>{{ propertiesStore.error }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-page {
  @apply min-h-screen bg-base-200;
}

/* Hero Section */
.hero-section {
  @apply relative bg-gradient-to-br from-primary to-secondary;
  @apply text-white py-16 mb-8;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  @apply absolute inset-0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  animation: backgroundShift 10s ease-in-out infinite;
}

.hero-content {
  @apply container mx-auto px-4 relative z-10 text-center;
}

.hero-title {
  @apply text-4xl md:text-5xl lg:text-6xl font-bold mb-4;
  font-feature-settings: 'ss01', 'ss02';
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 0.8s ease-out;
}

.hero-subtitle {
  @apply text-lg md:text-xl text-white/90;
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

/* Results Header */
.results-header {
  @apply flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6;
}

.results-info {
  @apply flex-1;
}

.results-count {
  @apply text-2xl md:text-3xl font-bold text-base-content;
  font-feature-settings: 'ss01', 'ss02';
}

.results-location {
  @apply text-base-content/60 mt-1;
}

.sort-control {
  @apply flex items-center gap-3;
}

.sort-label {
  @apply text-sm font-medium text-base-content/70;
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes backgroundShift {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(20px, 20px) scale(1.05);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    @apply text-3xl;
  }
  
  .results-count {
    @apply text-xl;
  }
}
</style>
