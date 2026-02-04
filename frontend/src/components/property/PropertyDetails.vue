<script setup lang="ts">
import { computed } from 'vue'
import type { Property } from '@/types/property'

const props = defineProps<{
  property: Property
}>()

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

const formatDate = (dateString?: string) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Computed sections
const keyFacts = computed(() => [
  {
    label: 'Price',
    value: formatPrice(props.property.list_price),
    icon: 'currency'
  },
  {
    label: 'Bedrooms',
    value: props.property.beds,
    icon: 'bed'
  },
  {
    label: 'Bathrooms',
    value: props.property.full_baths + (props.property.half_baths || 0),
    icon: 'bath'
  },
  {
    label: 'Square Feet',
    value: props.property.sqft ? formatNumber(props.property.sqft) : 'N/A',
    icon: 'ruler'
  },
  {
    label: 'Price per Sq Ft',
    value: props.property.price_per_sqft ? formatPrice(props.property.price_per_sqft) : 'N/A',
    icon: 'calculator'
  },
  {
    label: 'Lot Size',
    value: props.property.lot_sqft ? `${formatNumber(props.property.lot_sqft)} sq ft` : 'N/A',
    icon: 'land'
  }
])

const propertyInfo = computed(() => [
  { label: 'Property Type', value: props.property.property_type || 'N/A' },
  { label: 'Year Built', value: props.property.year_built || 'N/A' },
  { label: 'Style', value: props.property.style || 'N/A' },
  { label: 'Parking', value: props.property.parking_garage ? `${props.property.parking_garage} car garage` : 'N/A' },
  { label: 'HOA Fee', value: props.property.hoa_fee ? `${formatPrice(props.property.hoa_fee)}/month` : 'None' }
])

const listingInfo = computed(() => [
  { label: 'MLS ID', value: props.property.mls_id || 'N/A' },
  { label: 'Status', value: props.property.status || 'N/A' },
  { label: 'Days on Market', value: props.property.days_on_mls || 'N/A' },
  { label: 'List Date', value: formatDate(props.property.list_date) },
  { label: 'Last Sold', value: formatDate(props.property.last_sold_date) },
  { label: 'Last Sold Price', value: props.property.last_sold_price ? formatPrice(props.property.last_sold_price) : 'N/A' }
])

const getIcon = (iconName: string) => {
  const icons: Record<string, string> = {
    currency: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    bed: 'M3 10h18M3 14h18m-9-4v8m-7 0V8a2 2 0 012-2h10a2 2 0 012 2v10',
    bath: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
    ruler: 'M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4',
    calculator: 'M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z',
    land: 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
  }
  return icons[iconName] || icons.currency
}
</script>

<template>
  <div class="property-details">
    <!-- Key Facts Section -->
    <section class="details-section">
      <h2 class="section-title">Key Facts</h2>
      
      <div class="key-facts-grid">
        <div
          v-for="fact in keyFacts"
          :key="fact.label"
          class="fact-card"
        >
          <div class="fact-icon">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getIcon(fact.icon)" />
            </svg>
          </div>
          <div class="fact-content">
            <p class="fact-label">{{ fact.label }}</p>
            <p class="fact-value">{{ fact.value }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Description -->
    <section v-if="property.description" class="details-section">
      <h2 class="section-title">Property Description</h2>
      <div class="description-content">
        <p class="description-text">{{ property.description }}</p>
      </div>
    </section>

    <!-- Property Information -->
    <section class="details-section">
      <h2 class="section-title">Property Information</h2>
      
      <div class="info-grid">
        <div
          v-for="info in propertyInfo"
          :key="info.label"
          class="info-row"
        >
          <span class="info-label">{{ info.label }}</span>
          <span class="info-value">{{ info.value }}</span>
        </div>
      </div>
    </section>

    <!-- Listing Details -->
    <section class="details-section">
      <h2 class="section-title">Listing Details</h2>
      
      <div class="info-grid">
        <div
          v-for="info in listingInfo"
          :key="info.label"
          class="info-row"
        >
          <span class="info-label">{{ info.label }}</span>
          <span class="info-value">{{ info.value }}</span>
        </div>
      </div>
    </section>

    <!-- Agent Information -->
    <section v-if="property.listing_agent || property.listing_office" class="details-section">
      <h2 class="section-title">Agent Information</h2>
      
      <div class="agent-card">
        <div class="agent-avatar">
          <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
          </svg>
        </div>
        <div class="agent-info">
          <h3 class="agent-name">{{ property.listing_agent || 'Contact Agent' }}</h3>
          <p v-if="property.listing_office" class="agent-office">{{ property.listing_office }}</p>
          <button class="btn btn-primary btn-sm mt-3">
            Contact Agent
          </button>
        </div>
      </div>
    </section>

    <!-- Location -->
    <section class="details-section">
      <h2 class="section-title">Location</h2>
      
      <div class="location-info">
        <div class="location-icon">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <div>
          <p class="location-address">{{ property.full_street_line }}</p>
          <p class="location-city">{{ property.city }}, {{ property.state }} {{ property.zip_code }}</p>
          <p v-if="property.county" class="location-county">{{ property.county }} County</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.property-details {
  @apply space-y-8;
}

/* Section Styles */
.details-section {
  @apply bg-white rounded-xl p-6 shadow-sm;
  border: 1px solid hsl(var(--b2));
}

.section-title {
  @apply text-2xl font-bold text-base-content mb-6;
  font-feature-settings: 'ss01', 'ss02';
}

/* Key Facts Grid */
.key-facts-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4;
}

.fact-card {
  @apply flex items-start gap-4 p-4 rounded-lg;
  @apply bg-gradient-to-br from-base-100 to-base-200;
  @apply border border-base-300;
  @apply transition-all duration-300;
  @apply hover:shadow-md hover:scale-105;
}

.fact-icon {
  @apply flex-shrink-0;
  @apply w-12 h-12 rounded-full;
  @apply bg-primary/10 text-primary;
  @apply flex items-center justify-center;
}

.fact-content {
  @apply flex-1;
}

.fact-label {
  @apply text-sm text-base-content/60 mb-1;
}

.fact-value {
  @apply text-xl font-bold text-base-content;
}

/* Description */
.description-content {
  @apply prose prose-lg max-w-none;
}

.description-text {
  @apply text-base-content/80 leading-relaxed;
  @apply whitespace-pre-line;
}

/* Info Grid */
.info-grid {
  @apply space-y-3;
}

.info-row {
  @apply flex justify-between items-center py-3;
  @apply border-b border-base-200 last:border-0;
}

.info-label {
  @apply text-base-content/60 font-medium;
}

.info-value {
  @apply text-base-content font-semibold;
  @apply capitalize;
}

/* Agent Card */
.agent-card {
  @apply flex items-center gap-6 p-6;
  @apply bg-gradient-to-br from-primary/5 to-secondary/5;
  @apply rounded-xl border border-primary/20;
}

.agent-avatar {
  @apply w-20 h-20 rounded-full;
  @apply bg-primary/10 text-primary;
  @apply flex items-center justify-center;
}

.agent-info {
  @apply flex-1;
}

.agent-name {
  @apply text-xl font-bold text-base-content;
}

.agent-office {
  @apply text-base-content/60 mt-1;
}

/* Location */
.location-info {
  @apply flex items-start gap-4;
}

.location-icon {
  @apply flex-shrink-0;
  @apply w-12 h-12 rounded-full;
  @apply bg-error/10 text-error;
  @apply flex items-center justify-center;
}

.location-address {
  @apply text-lg font-semibold text-base-content;
}

.location-city {
  @apply text-base-content/70 mt-1;
}

.location-county {
  @apply text-sm text-base-content/50 mt-1;
}

/* Responsive */
@media (max-width: 768px) {
  .key-facts-grid {
    @apply grid-cols-1;
  }
  
  .fact-card {
    @apply p-3;
  }
  
  .agent-card {
    @apply flex-col text-center;
  }
}
</style>
