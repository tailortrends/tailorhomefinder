<template>
  <div class="home" :class="{ 'has-comparison': comparisonStore.comparisonList.length > 0 }">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-background" />
      <div class="hero-overlay" />
      
      <div class="container hero-content">
        <p class="hero-subtitle">Exclusive Portfolio</p>
        <h1 class="hero-title">
          Find Your <br/>
          <span class="hero-title-accent">Dream Home</span>
        </h1>
        <p class="hero-description">
          Search thousands of homes for sale and for rent across Arizona
        </p>
        
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

      <div class="scroll-indicator">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 5v14"/>
          <path d="m19 12-7 7-7-7"/>
        </svg>
      </div>
    </section>

    <!-- Featured Properties -->
    <section class="featured-properties container" id="listings">
      <div class="section-header">
        <h2>Featured Properties</h2>
        <p class="section-subtitle">{{ propertiesStore.properties.length }} properties available</p>
      </div>

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

      <!-- Properties Grid -->
      <div v-else-if="propertiesStore.properties.length > 0" class="properties-grid">
        <PropertyCard
          v-for="property in propertiesStore.properties"
          :key="property.id"
          :property="property"
          @select="handlePropertySelect"
        />
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
          <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
          <polyline points="9 22 9 12 15 12 15 22"/>
        </svg>
        <h3>No properties available</h3>
        <p>Try adjusting your search or check back later for new listings.</p>
      </div>
    </section>

        <!-- Add before closing </div> -->
    <ComparisonBar @open-comparison="comparisonModalOpen = true" />
    <ComparisonModal :is-open="comparisonModalOpen" @close="comparisonModalOpen = false" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import PropertyCard from '@/components/property/PropertyCard.vue'
import ComparisonBar from '@/components/comparison/ComparisonBar.vue'
import ComparisonModal from '@/components/comparison/ComparisonModal.vue'
import { useComparisonStore } from '@/stores/comparison'

const router = useRouter();
const propertiesStore = usePropertiesStore();
const searchQuery = ref('');

const comparisonModalOpen = ref(false)
const comparisonStore = useComparisonStore()

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ 
      name: 'search', 
      query: { q: searchQuery.value } 
    });
  }
};

const handlePropertySelect = (property: Property) => {
  router.push({
    name: 'property-detail',
    params: { id: property.id }
  });
};

onMounted(() => {
  propertiesStore.fetchProperties();
});
</script>

<style scoped>
.hero {
  position: relative;
  height: 80vh;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  inset: 0;
  background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1920&h=1080&fit=crop');
  background-size: cover;
  background-position: center;
  animation: kenburns 20s infinite alternate;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, var(--color-background) 0%, rgba(0, 0, 0, 0.6) 50%, rgba(0, 0, 0, 0.4) 100%);
}

.hero-content {
  position: relative;
  z-index: 10;
  text-align: center;
  color: white;
  max-width: 900px;
}

.hero-subtitle {
  color: var(--color-gold-400);
  font-size: var(--font-size-sm);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3em;
  margin-bottom: 1rem;
}

.hero-title {
  font-family: var(--font-family-display);
  font-size: clamp(2.5rem, 8vw, 5rem);
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.hero-title-accent {
  font-family: var(--font-family-serif);
  font-style: italic;
  color: var(--color-gold-400);
}

.hero-description {
  font-family: var(--font-family-serif);
  font-size: var(--font-size-lg);
  font-style: italic;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 2.5rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.search-bar {
  display: flex;
  gap: 0.75rem;
  max-width: 700px;
  margin: 0 auto;
}

.search-bar input {
  flex: 1;
  padding: 1rem 1.5rem;
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  background: white;
  color: #000;
}

.search-bar input::placeholder {
  color: #6b7280;
}

.search-bar input:focus {
  outline: 2px solid var(--color-gold-500);
  outline-offset: 2px;
}

.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  animation: bounce 2s infinite;
}

.scroll-indicator svg {
  color: rgba(255, 255, 255, 0.6);
}

@keyframes bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(10px); }
}

.featured-properties {
  padding: 4rem 0;
}

.section-header {
  margin-bottom: 3rem;
}

.section-header h2 {
  font-family: var(--font-family-display);
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.5rem;
}

.section-subtitle {
  color: var(--color-text-secondary);
  font-size: var(--font-size-lg);
}

.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
}

.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-state p {
  color: var(--color-text-secondary);
}

.error-state {
  color: var(--color-error);
}

.error-state button {
  margin-top: 1rem;
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
}

@media (max-width: 768px) {
  .hero {
    height: 70vh;
    min-height: 500px;
  }

  .search-bar {
    flex-direction: column;
  }

  .properties-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  .home-page {
    padding-bottom: 0;
    transition: padding-bottom 0.3s ease;
  }

  .home-page.has-comparison {
    padding-bottom: 120px;
  }
}

</style>