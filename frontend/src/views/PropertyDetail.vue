<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { useComparisonStore } from '@/stores/comparison'
import ImageGallery from '@/components/property/ImageGallery.vue'
import PropertyDetails from '@/components/property/PropertyDetails.vue'
import SimilarProperties from '@/components/property/SimilarProperties.vue'
import ContactForm from '@/components/property/ContactForm.vue'
import MapView from '@/components/property/MapView.vue'
import PriceHistoryChart from '@/components/property/PriceHistoryChart.vue'

const route = useRoute()
const router = useRouter()
const propertiesStore = usePropertiesStore()
const comparisonStore = useComparisonStore()

const propertyId = computed(() => route.params.id as string)
const property = computed(() => propertiesStore.currentProperty)
const loading = ref(true)
const error = ref<string | null>(null)

// Fetch property data
onMounted(async () => {
  try {
    loading.value = true
    error.value = null
    
    await propertiesStore.fetchPropertyById(propertyId.value)
    
    if (!propertiesStore.currentProperty) {
      error.value = 'Property not found'
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load property'
  } finally {
    loading.value = false
  }
})

// Format helpers
const formatPrice = (price: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(price)
}

const formatNumber = (num: number) => {
  return new Intl.NumberFormat('en-US').format(num)
}

// Images for gallery
const propertyImages = computed(() => {
  if (!property.value) return []
  
  const images: string[] = []
  
  if (property.value.primary_photo) {
    images.push(property.value.primary_photo)
  }
  
  if (property.value.photos && property.value.photos.length > 0) {
    images.push(...property.value.photos.filter(p => p !== property.value.primary_photo))
  }
  
  // If no images, return placeholder
  if (images.length === 0) {
    images.push('https://via.placeholder.com/1200x800?text=No+Image+Available')
  }
  
  return images
})

// Comparison actions
const isInComparison = computed(() => {
  if (!property.value) return false
  return comparisonStore.properties.some(p => p.property_id === property.value!.property_id)
})

function toggleComparison() {
  if (!property.value) return
  
  if (isInComparison.value) {
    comparisonStore.removeProperty(property.value.property_id)
  } else {
    comparisonStore.addProperty(property.value)
  }
}

// Contact form handler
function handleContactSubmit(data: any) {
  console.log('Contact form submitted:', data)
  // In production, this would send to your backend API
}

// Favorite action (placeholder)
const isFavorite = ref(false)

function toggleFavorite() {
  isFavorite.value = !isFavorite.value
  // In production, this would call your favorites API
}

// Share action
function shareProperty() {
  if (navigator.share) {
    navigator.share({
      title: property.value?.full_street_line || 'Property',
      text: `Check out this property: ${property.value?.full_street_line}`,
      url: window.location.href
    })
  } else {
    // Fallback: copy to clipboard
    navigator.clipboard.writeText(window.location.href)
    alert('Link copied to clipboard!')
  }
}

// Back navigation
function goBack() {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/search')
  }
}
</script>

<template>
  <div class="property-detail-page">
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading loading-spinner loading-lg text-primary"></div>
      <p class="loading-text">Loading property details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error || !property" class="error-container">
      <svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h2 class="error-title">Property Not Found</h2>
      <p class="error-message">{{ error || 'The property you\'re looking for doesn\'t exist.' }}</p>
      <button class="btn btn-primary mt-4" @click="$router.push('/search')">
        Back to Search
      </button>
    </div>

    <!-- Property Content -->
    <div v-else class="property-content">
      <!-- Back Button -->
      <div class="container mx-auto px-4 pt-6">
        <button class="back-btn" @click="goBack">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Back to Results
        </button>
      </div>

      <!-- Property Header -->
      <div class="property-header">
        <div class="container mx-auto px-4 py-6">
          <div class="header-content">
            <div class="header-main">
              <h1 class="property-title">{{ property.full_street_line }}</h1>
              <p class="property-location">
                {{ property.city }}, {{ property.state }} {{ property.zip_code }}
              </p>
            </div>
            
            <div class="header-actions">
              <button
                class="action-btn"
                :class="{ 'action-btn-active': isFavorite }"
                @click="toggleFavorite"
              >
                <svg class="w-6 h-6" :fill="isFavorite ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
                <span class="action-label">Save</span>
              </button>

              <button class="action-btn" @click="shareProperty">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                </svg>
                <span class="action-label">Share</span>
              </button>

              <button
                class="action-btn"
                :class="{ 'action-btn-active': isInComparison }"
                @click="toggleComparison"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
                <span class="action-label">Compare</span>
              </button>
            </div>
          </div>

          <!-- Price and Quick Stats -->
          <div class="quick-stats">
            <div class="price-section">
              <p class="price-label">List Price</p>
              <h2 class="price-value">{{ formatPrice(property.list_price) }}</h2>
              <p v-if="property.price_per_sqft" class="price-per-sqft">
                {{ formatPrice(property.price_per_sqft) }} per sq ft
              </p>
            </div>

            <div class="stats-grid">
              <div class="stat-item">
                <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a2 2 0 001 1h3m10-11l2 2m-2-2v10a2 2 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                <span class="stat-value">{{ property.beds }}</span>
                <span class="stat-label">Beds</span>
              </div>

              <div class="stat-item">
                <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span class="stat-value">{{ property.full_baths }}</span>
                <span class="stat-label">Baths</span>
              </div>

              <div v-if="property.sqft" class="stat-item">
                <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                </svg>
                <span class="stat-value">{{ formatNumber(property.sqft) }}</span>
                <span class="stat-label">Sq Ft</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="container mx-auto px-4 py-8">
        <div class="content-grid">
          <!-- Left Column -->
          <div class="left-column">
            <!-- Image Gallery -->
            <ImageGallery
              :images="propertyImages"
              :property-title="property.full_street_line"
            />

            <!-- Property Details -->
            <PropertyDetails :property="property" />

            <!-- Map (if MapView component exists) -->
            <div v-if="property.latitude && property.longitude" class="map-section">
              <h2 class="section-title">Location</h2>
              <MapView
                :latitude="property.latitude"
                :longitude="property.longitude"
                :address="property.full_street_line"
              />
            </div>

            <!-- Price History Chart (if available) -->
            <div v-if="property.last_sold_price" class="chart-section">
              <h2 class="section-title">Price History</h2>
              <PriceHistoryChart
                :current-price="property.list_price"
                :last-sold-price="property.last_sold_price"
                :last-sold-date="property.last_sold_date"
              />
            </div>
          </div>

          <!-- Right Column - Contact Form -->
          <div class="right-column">
            <ContactForm
              :property="property"
              @submit="handleContactSubmit"
            />
          </div>
        </div>

        <!-- Similar Properties -->
        <div class="similar-section">
          <SimilarProperties
            :current-property="property"
            :all-properties="propertiesStore.properties"
            :max-results="6"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.property-detail-page {
  @apply min-h-screen bg-base-200;
}

/* Loading & Error States */
.loading-container,
.error-container {
  @apply flex flex-col items-center justify-center min-h-screen;
  @apply py-20 px-4;
}

.loading-text {
  @apply text-base-content/60 mt-4;
}

.error-icon {
  @apply w-20 h-20 text-error mb-4;
}

.error-title {
  @apply text-3xl font-bold text-base-content mb-2;
}

.error-message {
  @apply text-base-content/60 text-center max-w-md;
}

/* Back Button */
.back-btn {
  @apply flex items-center gap-2;
  @apply text-base-content/70 hover:text-primary;
  @apply font-medium transition-colors;
}

/* Property Header */
.property-header {
  @apply bg-white border-b border-base-200;
  @apply shadow-sm;
}

.header-content {
  @apply flex flex-col md:flex-row justify-between items-start md:items-center gap-4;
}

.header-main {
  @apply flex-1;
}

.property-title {
  @apply text-3xl md:text-4xl font-bold text-base-content mb-2;
  font-feature-settings: 'ss01', 'ss02';
}

.property-location {
  @apply text-lg text-base-content/60;
}

/* Header Actions */
.header-actions {
  @apply flex gap-2;
}

.action-btn {
  @apply flex flex-col items-center gap-1;
  @apply px-4 py-3 rounded-lg;
  @apply bg-base-100 hover:bg-base-200;
  @apply border border-base-300;
  @apply transition-all duration-300;
}

.action-btn-active {
  @apply bg-primary text-white border-primary;
}

.action-label {
  @apply text-xs font-medium;
}

/* Quick Stats */
.quick-stats {
  @apply flex flex-col md:flex-row gap-6 mt-6 pt-6 border-t border-base-200;
}

.price-section {
  @apply flex-1;
}

.price-label {
  @apply text-sm text-base-content/60 mb-1;
}

.price-value {
  @apply text-4xl font-bold text-primary;
  font-feature-settings: 'ss01', 'ss02';
}

.price-per-sqft {
  @apply text-sm text-base-content/60 mt-1;
}

.stats-grid {
  @apply flex gap-8;
}

.stat-item {
  @apply flex flex-col items-center;
}

.stat-icon {
  @apply w-8 h-8 text-base-content/40 mb-2;
}

.stat-value {
  @apply text-2xl font-bold text-base-content;
}

.stat-label {
  @apply text-sm text-base-content/60;
}

/* Content Grid */
.content-grid {
  @apply grid grid-cols-1 lg:grid-cols-3 gap-8;
}

.left-column {
  @apply lg:col-span-2 space-y-8;
}

.right-column {
  @apply lg:col-span-1;
}

.map-section,
.chart-section {
  @apply bg-white rounded-xl p-6 shadow-sm;
  border: 1px solid hsl(var(--b2));
}

.section-title {
  @apply text-2xl font-bold text-base-content mb-6;
  font-feature-settings: 'ss01', 'ss02';
}

.similar-section {
  @apply mt-12;
}

/* Responsive */
@media (max-width: 1024px) {
  .content-grid {
    @apply grid-cols-1;
  }
  
  .right-column {
    @apply order-first lg:order-last;
  }
}

@media (max-width: 768px) {
  .property-title {
    @apply text-2xl;
  }
  
  .stats-grid {
    @apply gap-4;
  }
  
  .header-actions {
    @apply w-full justify-between;
  }
}
</style>
