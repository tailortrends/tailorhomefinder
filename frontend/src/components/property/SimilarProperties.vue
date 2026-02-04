<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import type { Property } from '@/types/property'
import PropertyCard from './PropertyCard.vue'

const props = defineProps<{
  currentProperty: Property
  allProperties: Property[]
  maxResults?: number
}>()

const router = useRouter()

// Find similar properties based on multiple criteria
const similarProperties = computed(() => {
  const similar = props.allProperties
    .filter(p => p.property_id !== props.currentProperty.property_id) // Exclude current property
    .map(property => {
      let score = 0
      
      // Same city (highest weight)
      if (property.city === props.currentProperty.city) score += 40
      
      // Similar price range (±20%)
      const priceDiff = Math.abs(property.list_price - props.currentProperty.list_price)
      const priceRange = props.currentProperty.list_price * 0.2
      if (priceDiff <= priceRange) score += 30
      
      // Same number of bedrooms
      if (property.beds === props.currentProperty.beds) score += 15
      
      // Similar square footage (±20%)
      if (property.sqft && props.currentProperty.sqft) {
        const sqftDiff = Math.abs(property.sqft - props.currentProperty.sqft)
        const sqftRange = props.currentProperty.sqft * 0.2
        if (sqftDiff <= sqftRange) score += 10
      }
      
      // Same property type
      if (property.property_type === props.currentProperty.property_type) score += 5
      
      return { property, score }
    })
    .filter(item => item.score > 20) // Only show properties with reasonable similarity
    .sort((a, b) => b.score - a.score) // Sort by similarity score
    .slice(0, props.maxResults || 6) // Limit results
    .map(item => item.property)
  
  return similar
})

const hasSimilarProperties = computed(() => similarProperties.value.length > 0)

function handlePropertyClick(property: Property) {
  router.push({
    name: 'property-detail',
    params: { id: property.property_id }
  })
  
  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
  <div v-if="hasSimilarProperties" class="similar-properties">
    <!-- Section Header -->
    <div class="section-header">
      <div>
        <h2 class="section-title">Similar Properties</h2>
        <p class="section-subtitle">
          You might also be interested in these homes
        </p>
      </div>
      
      <div class="similarity-badge">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ similarProperties.length }} Matches
      </div>
    </div>

    <!-- Properties Grid -->
    <div class="properties-grid">
      <PropertyCard
        v-for="property in similarProperties"
        :key="property.property_id"
        :property="property"
        class="similar-card"
        @click="handlePropertyClick(property)"
      />
    </div>

    <!-- View More Button -->
    <div class="view-more-container">
      <button class="btn btn-outline btn-lg" @click="$router.push('/search')">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        View All Properties
      </button>
    </div>
  </div>

  <!-- No Similar Properties Message -->
  <div v-else class="no-similar">
    <div class="no-similar-content">
      <svg class="no-similar-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
      <h3 class="no-similar-title">No Similar Properties Found</h3>
      <p class="no-similar-text">
        This property is unique! Browse our full catalog to find other great homes.
      </p>
      <button class="btn btn-primary mt-4" @click="$router.push('/search')">
        Browse All Properties
      </button>
    </div>
  </div>
</template>

<style scoped>
.similar-properties {
  @apply bg-white rounded-xl p-6 shadow-sm;
  border: 1px solid hsl(var(--b2));
}

/* Section Header */
.section-header {
  @apply flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8;
}

.section-title {
  @apply text-2xl md:text-3xl font-bold text-base-content;
  font-feature-settings: 'ss01', 'ss02';
}

.section-subtitle {
  @apply text-base-content/60 mt-1;
}

.similarity-badge {
  @apply flex items-center gap-2;
  @apply bg-primary/10 text-primary;
  @apply px-4 py-2 rounded-full;
  @apply font-semibold text-sm;
  @apply whitespace-nowrap;
}

/* Properties Grid */
.properties-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6;
}

.similar-card {
  @apply opacity-0;
  animation: fadeInUp 0.6s ease-out forwards;
}

.similar-card:nth-child(1) { animation-delay: 0.1s; }
.similar-card:nth-child(2) { animation-delay: 0.2s; }
.similar-card:nth-child(3) { animation-delay: 0.3s; }
.similar-card:nth-child(4) { animation-delay: 0.4s; }
.similar-card:nth-child(5) { animation-delay: 0.5s; }
.similar-card:nth-child(6) { animation-delay: 0.6s; }

/* View More */
.view-more-container {
  @apply flex justify-center mt-8;
}

/* No Similar Properties */
.no-similar {
  @apply bg-white rounded-xl p-12 shadow-sm;
  @apply border-2 border-dashed border-base-300;
}

.no-similar-content {
  @apply flex flex-col items-center text-center;
  @apply max-w-md mx-auto;
}

.no-similar-icon {
  @apply w-20 h-20 text-base-300 mb-4;
}

.no-similar-title {
  @apply text-xl font-bold text-base-content mb-2;
}

.no-similar-text {
  @apply text-base-content/60;
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

/* Responsive */
@media (max-width: 768px) {
  .properties-grid {
    @apply grid-cols-1;
  }
  
  .section-header {
    @apply flex-col items-start;
  }
}
</style>
