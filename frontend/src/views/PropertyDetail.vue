<template>
  <div class="property-detail">
    <!-- Loading State -->
    <div v-if="propertiesStore.loading" class="loading-state container">
      <div class="spinner"></div>
      <p>Loading property details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="propertiesStore.error" class="error-state container">
      <p>{{ propertiesStore.error }}</p>
      <button class="btn btn-primary" @click="router.push({ name: 'home' })">
        Back to Home
      </button>
    </div>

    <!-- Property Not Found -->
    <div v-else-if="!property" class="error-state container">
      <h2>Property not found</h2>
      <button class="btn btn-primary" @click="router.push({ name: 'home' })">
        Back to Home
      </button>
    </div>

    <!-- Property Content -->
    <div v-else>
      <!-- Hero Image -->
      <!-- Image Gallery -->
    <section class="gallery" @click="openLightbox(0)">
      <div class="main-image">
        <img 
          v-if="property.images && property.images.length > 0"
          :src="property.images[0]" 
          :alt="property.address"
        />
        <div v-else class="no-image">No Image Available</div>
        
        <!-- Gallery indicator if multiple images -->
        <div v-if="allImages.length > 1" class="gallery-indicator">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
            <circle cx="9" cy="9" r="2"/>
            <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
          </svg>
          <span>{{ allImages.length }} photos</span>
        </div>
      </div>
    </section>

    <!-- Add Lightbox at the end of template, before closing div -->
    <ImageLightbox 
      v-if="property"
      :images="allImages"
      :initial-index="lightboxIndex"
      :is-open="lightboxOpen"
      @close="lightboxOpen = false"
    />

      <!-- Property Details -->
      <section class="property-info container">
        <div class="info-layout">
          <!-- Main Content -->
          <main class="main-content">
            <!-- Price & Stats -->
            <div class="price-stats-section">
              <div class="price-block">
                <span class="price-label">Price</span>
                <span class="price-value">{{ formatPrice(property.price) }}</span>
              </div>
              
              <div class="stats-grid">
                <div class="stat-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 9h18v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9Z"/>
                    <path d="M3 9V7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v2"/>
                  </svg>
                  <div>
                    <span class="stat-value">{{ property.beds || '-' }}</span>
                    <span class="stat-label">Bedrooms</span>
                  </div>
                </div>
                
                <div class="stat-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-1 0l-1 1a1.5 1.5 0 0 0 0 1L7 9"/>
                    <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                  </svg>
                  <div>
                    <span class="stat-value">{{ property.baths || '-' }}</span>
                    <span class="stat-label">Bathrooms</span>
                  </div>
                </div>
                
                <div class="stat-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15V6"/>
                    <path d="M18.5 18a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z"/>
                    <path d="M12 12H3"/>
                    <path d="M16 6H3"/>
                    <path d="M12 18H3"/>
                  </svg>
                  <div>
                    <span class="stat-value">{{ property.sqft?.toLocaleString() || '-' }}</span>
                    <span class="stat-label">Sq Ft</span>
                  </div>
                </div>
                
                <div class="stat-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect width="18" height="18" x="3" y="3" rx="2"/>
                    <path d="M3 9h18"/>
                    <path d="M9 21V9"/>
                  </svg>
                  <div>
                    <span class="stat-value">{{ property.yearBuilt || '-' }}</span>
                    <span class="stat-label">Year Built</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Description -->
            <div class="section-block">
              <h2 class="section-title">About This Property</h2>
              <p class="property-description">{{ property.description }}</p>
            </div>

            <!-- Features -->
            <div v-if="property.features && property.features.length > 0" class="section-block">
              <h2 class="section-title">Features</h2>
              <div class="features-grid">
                <div 
                  v-for="(feature, idx) in property.features" 
                  :key="idx"
                  class="feature-item"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 6 9 17l-5-5"/>
                  </svg>
                  {{ feature }}
                </div>
              </div>
            </div>

            <!-- Price History Chart -->
            <div v-if="property.history && property.history.length > 1" class="section-block">
              <h2 class="section-title">Price History</h2>
              <PriceHistoryChart :history="property.history" />
              <p class="chart-note">
                Historical valuations based on listing data
              </p>
            </div>

            <!-- Additional Details -->
            <div class="section-block">
              <h2 class="section-title">Property Details</h2>
              <div class="details-grid">
                <div class="detail-row">
                  <span class="detail-label">Property Type:</span>
                  <span class="detail-value">{{ property.type }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Status:</span>
                  <span class="detail-value">{{ property.status || 'N/A' }}</span>
                </div>
                <div v-if="property.lotSqft" class="detail-row">
                  <span class="detail-label">Lot Size:</span>
                  <span class="detail-value">{{ property.lotSqft.toLocaleString() }} sq ft</span>
                </div>
                <div v-if="property.hoaFee" class="detail-row">
                  <span class="detail-label">HOA Fee:</span>
                  <span class="detail-value">${{ property.hoaFee }}/month</span>
                </div>
                <div v-if="property.agentName" class="detail-row">
                  <span class="detail-label">Agent:</span>
                  <span class="detail-value">{{ property.agentName }}</span>
                </div>
                <div v-if="property.officeName" class="detail-row">
                  <span class="detail-label">Office:</span>
                  <span class="detail-value">{{ property.officeName }}</span>
                </div>
              </div>
            </div>
          </main>

          <!-- Sidebar -->
          <aside class="sidebar">
            <div class="contact-card">
              <h3>Interested in this property?</h3>
              <p class="contact-description">Contact us to schedule a viewing or get more information.</p>
              <button class="btn btn-primary full-width">Schedule Tour</button>
              <button class="btn btn-secondary full-width">Contact Agent</button>
              
              <a 
                v-if="property.propertyUrl"
                :href="property.propertyUrl"
                target="_blank"
                rel="noopener noreferrer"
                class="external-link"
              >
                View on Realtor.com
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                  <path d="M15 3h6v6"/>
                  <path d="M10 14 21 3"/>
                </svg>
              </a>
            </div>
          </aside>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { formatPrice } from '@/utils/propertyHelpers'
import PriceHistoryChart from '@/components/property/PriceHistoryChart.vue'
import ImageLightbox from '@/components/common/ImageLightbox.vue'

const route = useRoute()
const router = useRouter()
const propertiesStore = usePropertiesStore()

const property = computed(() => propertiesStore.selectedProperty)

// Lightbox state
const lightboxOpen = ref(false)
const lightboxIndex = ref(0)

const allImages = computed(() => {
  if (!property.value) return []
  const images = [property.value.image]
  if (property.value.altPhotos && property.value.altPhotos.length > 0) {
    images.push(...property.value.altPhotos)
  }
  return images
})

const openLightbox = (index: number) => {
  lightboxIndex.value = index
  lightboxOpen.value = true
}

onMounted(() => {
  const propertyId = route.params.id as string
  propertiesStore.fetchPropertyById(propertyId)
})
</script>

<style scoped>
.property-hero {
  position: relative;
  height: 60vh;
  min-height: 400px;
  overflow: hidden;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.4) 50%, transparent 100%);
}

.hero-content {
  position: absolute;
  bottom: 2rem;
  left: 0;
  right: 0;
  color: white;
  z-index: 10;
}

.property-badges {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.badge-type {
  background: rgba(255, 255, 255, 0.9);
  color: var(--color-gold-600);
}

.badge-active {
  background: var(--color-success);
  color: white;
}

.badge-pending {
  background: var(--color-warning);
  color: white;
}

.property-title {
  font-family: var(--font-family-display);
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}

.property-location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: var(--font-size-lg);
}

.property-location svg {
  color: var(--color-gold-400);
}

.property-info {
  padding: 3rem 0;
}

.info-layout {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 3rem;
}

.price-stats-section {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 2rem;
  margin-bottom: 2rem;
}

.price-block {
  display: flex;
  flex-direction: column;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--color-border);
}

.price-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.5rem;
}

.price-value {
  font-family: var(--font-family-display);
  font-size: var(--font-size-4xl);
  font-weight: 700;
  color: var(--color-gold-500);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-item svg {
  color: var(--color-gold-500);
  flex-shrink: 0;
}

.stat-value {
  display: block;
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-text);
}

.stat-label {
  display: block;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.section-block {
  margin-bottom: 3rem;
}

.section-title {
  font-family: var(--font-family-display);
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-gold-500);
  margin-bottom: 1.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: var(--font-size-lg);
}

.property-description {
  font-size: var(--font-size-lg);
  line-height: 1.8;
  color: var(--color-text-secondary);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
}

.feature-item svg {
  color: var(--color-gold-500);
  flex-shrink: 0;
}

.details-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.detail-label {
  color: var(--color-text-secondary);
  font-weight: 500;
}

.detail-value {
  color: var(--color-text);
  font-weight: 600;
}

.sidebar {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.contact-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-lg);
}

.contact-card h3 {
  font-size: var(--font-size-xl);
  margin-bottom: 1rem;
  color: var(--color-text);
}

.contact-description {
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.full-width {
  width: 100%;
  margin-bottom: 0.75rem;
}

.external-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: var(--font-size-sm);
  border-top: 1px solid var(--color-border);
  margin-top: 1rem;
  padding-top: 1.5rem;
  transition: color 0.3s ease;
}

.external-link:hover {
  color: var(--color-gold-500);
}

.loading-state,
.error-state {
  text-align: center;
  padding: 4rem 2rem;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.error-state h2 {
  font-size: var(--font-size-2xl);
  margin-bottom: 1rem;
  color: var(--color-text);
}

@media (max-width: 768px) {
  .info-layout {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    position: static;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .chart-note {
  margin-top: 1rem;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  font-style: italic;
  text-align: right;
  }
  .gallery {
  cursor: pointer;
  position: relative;
}

.gallery-indicator {
  position: absolute;
  bottom: 1.5rem;
  right: 1.5rem;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.gallery:hover .gallery-indicator {
  background: rgba(212, 175, 55, 0.9);
  transform: scale(1.05);
}

.gallery-indicator svg {
  width: 18px;
  height: 18px;
}
}
</style>