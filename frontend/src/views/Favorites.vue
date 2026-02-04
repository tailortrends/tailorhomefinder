<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFavoritesStore } from '@/stores/favorites'
import PropertyCard from '@/components/property/PropertyCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import type { Property } from '@/types/property'

const router = useRouter()
const favoritesStore = useFavoritesStore()

const sortBy = ref<'newest' | 'price_asc' | 'price_desc' | 'beds'>('newest')
const viewMode = ref<'grid' | 'list'>('grid')

// Load favorites on mount
onMounted(async () => {
  await favoritesStore.loadFavorites()
  applySorting(sortBy.value)
})

// Computed
const hasFavorites = computed(() => favoritesStore.hasFavorites)

const gridClass = computed(() => {
  if (viewMode.value === 'list') {
    return 'grid-cols-1'
  }
  return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
})

// Actions
function applySorting(sort: typeof sortBy.value) {
  switch (sort) {
    case 'newest':
      favoritesStore.sortByNewest()
      break
    case 'price_asc':
      favoritesStore.sortByPrice(true)
      break
    case 'price_desc':
      favoritesStore.sortByPrice(false)
      break
    case 'beds':
      favoritesStore.sortByBeds(false)
      break
  }
}

function handleSortChange(newSort: typeof sortBy.value) {
  sortBy.value = newSort
  applySorting(newSort)
}

function handlePropertyClick(property: Property) {
  router.push({
    name: 'property-detail',
    params: { id: property.property_id }
  })
}

function handleRemoveFavorite(propertyId: string) {
  if (confirm('Remove this property from your favorites?')) {
    favoritesStore.removeFavorite(propertyId)
  }
}

function handleClearAll() {
  if (confirm('Remove all properties from your favorites? This cannot be undone.')) {
    favoritesStore.clearFavorites()
  }
}

function goToSearch() {
  router.push('/search')
}
</script>

<template>
  <div class="favorites-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-main">
          <h1 class="hero-title">
            <svg class="inline w-10 h-10 mr-3 -mt-1" fill="currentColor" viewBox="0 0 24 24">
              <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            My Favorites
          </h1>
          <p class="hero-subtitle">
            {{ favoritesStore.favoritesCount }} saved 
            {{ favoritesStore.favoritesCount === 1 ? 'property' : 'properties' }}
          </p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-8">
      <!-- Loading State -->
      <div v-if="favoritesStore.loading && !hasFavorites" class="loading-container">
        <div class="loading loading-spinner loading-lg text-primary"></div>
        <p class="loading-text">Loading your favorites...</p>
      </div>

      <!-- Controls Bar -->
      <div v-else-if="hasFavorites" class="controls-bar">
        <div class="controls-left">
          <!-- View Toggle -->
          <div class="btn-group">
            <button
              class="btn btn-sm"
              :class="{ 'btn-active': viewMode === 'grid' }"
              @click="viewMode = 'grid'"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
              Grid
            </button>
            <button
              class="btn btn-sm"
              :class="{ 'btn-active': viewMode === 'list' }"
              @click="viewMode = 'list'"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              List
            </button>
          </div>

          <!-- Sort Dropdown -->
          <div class="sort-control">
            <label class="sort-label">Sort by:</label>
            <select
              :value="sortBy"
              class="select select-bordered select-sm"
              @change="(e) => handleSortChange((e.target as HTMLSelectElement).value as any)"
            >
              <option value="newest">Newest</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
              <option value="beds">Most Bedrooms</option>
            </select>
          </div>
        </div>

        <div class="controls-right">
          <button class="btn btn-ghost btn-sm" @click="handleClearAll">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Clear All
          </button>
        </div>
      </div>

      <!-- Favorites Grid -->
      <div v-if="hasFavorites" class="favorites-grid" :class="gridClass">
        <div
          v-for="property in favoritesStore.favorites"
          :key="property.property_id"
          class="favorite-item"
        >
          <PropertyCard
            :property="property"
            @click="handlePropertyClick(property)"
          />
          
          <!-- Remove Button Overlay -->
          <button
            class="remove-btn"
            @click.stop="handleRemoveFavorite(property.property_id)"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <EmptyState
        v-else-if="!favoritesStore.loading"
        title="No Favorites Yet"
        message="Start saving properties you love to view them here later."
        icon="home"
        action-text="Browse Properties"
        @action="goToSearch"
      />

      <!-- Error State -->
      <div v-if="favoritesStore.error" class="alert alert-error mt-6">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ favoritesStore.error }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.favorites-page {
  @apply min-h-screen bg-base-200;
}

/* Hero Section */
.hero-section {
  @apply relative bg-gradient-to-br from-error to-error/80;
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
  @apply container mx-auto px-4 relative z-10;
}

.hero-main {
  @apply text-center;
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

/* Loading */
.loading-container {
  @apply flex flex-col items-center justify-center py-20;
}

.loading-text {
  @apply text-base-content/60 mt-4;
}

/* Controls Bar */
.controls-bar {
  @apply flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6;
  @apply bg-white rounded-xl p-4 shadow-sm;
  border: 1px solid hsl(var(--b2));
}

.controls-left {
  @apply flex flex-wrap items-center gap-4;
}

.controls-right {
  @apply flex items-center gap-2;
}

.sort-control {
  @apply flex items-center gap-3;
}

.sort-label {
  @apply text-sm font-medium text-base-content/70;
}

/* Favorites Grid */
.favorites-grid {
  @apply grid gap-6;
}

.favorite-item {
  @apply relative;
  animation: fadeInUp 0.6s ease-out forwards;
}

.favorite-item:nth-child(1) { animation-delay: 0.1s; }
.favorite-item:nth-child(2) { animation-delay: 0.15s; }
.favorite-item:nth-child(3) { animation-delay: 0.2s; }
.favorite-item:nth-child(4) { animation-delay: 0.25s; }
.favorite-item:nth-child(5) { animation-delay: 0.3s; }
.favorite-item:nth-child(6) { animation-delay: 0.35s; }

/* Remove Button */
.remove-btn {
  @apply absolute top-3 right-3 z-10;
  @apply bg-white/95 backdrop-blur-sm;
  @apply text-error hover:bg-error hover:text-white;
  @apply p-2 rounded-full;
  @apply shadow-lg;
  @apply opacity-0 transition-all duration-300;
  @apply hover:scale-110;
}

.favorite-item:hover .remove-btn {
  @apply opacity-100;
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
  
  .controls-bar {
    @apply flex-col items-stretch;
  }
  
  .controls-left,
  .controls-right {
    @apply w-full justify-between;
  }
}
</style>
