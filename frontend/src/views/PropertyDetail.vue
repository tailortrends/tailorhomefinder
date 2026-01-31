<template>
  <div class="property-detail">
    <div v-if="propertiesStore.loading" class="loading container">
      Loading property details...
    </div>

    <div v-else-if="propertiesStore.error" class="error container">
      {{ propertiesStore.error }}
    </div>

    <div v-else-if="!property" class="error container">
      Property not found
    </div>

    <div v-else>
      <!-- Image Gallery -->
      <section class="gallery">
        <div class="main-image">
          <img 
            v-if="property.images && property.images.length > 0"
            :src="property.images[0]" 
            :alt="property.address"
          />
          <div v-else class="no-image">No Image Available</div>
        </div>
      </section>

      <!-- Property Info -->
      <section class="container property-info">
        <div class="info-layout">
          <main class="main-info">
            <div class="price">${{ property.price.toLocaleString() }}</div>
            <h1 class="address">{{ property.address }}</h1>
            <p class="location">{{ property.city }}, {{ property.state }} {{ property.zipCode }}</p>

            <div class="specs">
              <div class="spec-item">
                <strong>{{ property.bedrooms }}</strong> beds
              </div>
              <div class="spec-item">
                <strong>{{ property.bathrooms }}</strong> baths
              </div>
              <div class="spec-item">
                <strong>{{ property.squareFeet.toLocaleString() }}</strong> sqft
              </div>
              <div v-if="property.lotSize" class="spec-item">
                <strong>{{ property.lotSize.toLocaleString() }}</strong> lot sqft
              </div>
            </div>

            <div v-if="property.description" class="description">
              <h2>Description</h2>
              <p>{{ property.description }}</p>
            </div>

            <div v-if="property.features && property.features.length > 0" class="features">
              <h2>Features</h2>
              <ul>
                <li v-for="feature in property.features" :key="feature">
                  {{ feature }}
                </li>
              </ul>
            </div>

            <div class="details-grid">
              <div class="detail-item">
                <span class="label">Property Type:</span>
                <span class="value">{{ formatPropertyType(property.propertyType) }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Status:</span>
                <span class="value">{{ formatStatus(property.status) }}</span>
              </div>
              <div v-if="property.yearBuilt" class="detail-item">
                <span class="label">Year Built:</span>
                <span class="value">{{ property.yearBuilt }}</span>
              </div>
              <div v-if="property.listingDate" class="detail-item">
                <span class="label">Listed:</span>
                <span class="value">{{ formatDate(property.listingDate) }}</span>
              </div>
            </div>
          </main>

          <aside class="sidebar">
            <div class="contact-card">
              <h3>Interested in this property?</h3>
              <button class="btn btn-primary full-width">Contact Agent</button>
              <button class="btn full-width">Schedule Tour</button>
            </div>
          </aside>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'

const route = useRoute()
const propertiesStore = usePropertiesStore()

const property = computed(() => propertiesStore.selectedProperty)

const formatPropertyType = (type: string) => {
  return type.split('-').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}

const formatStatus = (status: string) => {
  return status.split('-').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}

const formatDate = (date: Date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  const propertyId = route.params.id as string
  propertiesStore.fetchPropertyById(propertyId)
})
</script>

<style scoped>
.gallery {
  background: var(--color-surface);
}

.main-image {
  max-width: 1280px;
  margin: 0 auto;
  height: 500px;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background: var(--color-border);
  color: var(--color-text-secondary);
}

.property-info {
  padding: var(--spacing-xl) 0;
}

.info-layout {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: var(--spacing-xl);
}

.price {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.address {
  font-size: var(--font-size-2xl);
  margin-bottom: var(--spacing-xs);
}

.location {
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-lg);
}

.specs {
  display: flex;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg) 0;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--spacing-xl);
}

.spec-item strong {
  display: block;
  font-size: var(--font-size-xl);
}

.description,
.features {
  margin-bottom: var(--spacing-xl);
}

.description h2,
.features h2 {
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-md);
}

.features ul {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--spacing-sm);
}

.features li:before {
  content: "✓ ";
  color: var(--color-success);
  margin-right: var(--spacing-xs);
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: var(--spacing-md);
  background: var(--color-surface);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
}

.detail-item {
  display: flex;
  justify-content: space-between;
}

.detail-item .label {
  color: var(--color-text-secondary);
}

.detail-item .value {
  font-weight: 500;
}

.sidebar {
  position: sticky;
  top: var(--spacing-lg);
  height: fit-content;
}

.contact-card {
  background: var(--color-surface);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.contact-card h3 {
  margin-bottom: var(--spacing-lg);
}

.full-width {
  width: 100%;
  margin-bottom: var(--spacing-sm);
}

.loading,
.error {
  padding: var(--spacing-xl);
  text-align: center;
}

.error {
  color: var(--color-error);
}

@media (max-width: 768px) {
  .info-layout {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    position: static;
  }
  
  .main-image {
    height: 300px;
  }
}
</style>