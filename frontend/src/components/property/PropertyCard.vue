<script setup lang="ts">
import { computed } from 'vue'
import type { Property } from '@/types/property'
import FavoriteButton from './FavoriteButton.vue'

const props = defineProps<{
  property: Property
}>()

const emit = defineEmits<{
  (e: 'click'): void
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

// Computed properties
const primaryImage = computed(() => {
  return props.property.primary_photo || 
         (props.property.photos && props.property.photos[0]) || 
         'https://via.placeholder.com/800x600?text=No+Image'
})

const bedsAndBaths = computed(() => {
  const beds = props.property.beds
  const baths = props.property.full_baths + (props.property.half_baths || 0)
  return `${beds} bd | ${baths} ba`
})

const squareFeet = computed(() => {
  if (!props.property.sqft) return null
  return `${formatNumber(props.property.sqft)} sqft`
})

const statusBadgeColor = computed(() => {
  const colors: Record<string, string> = {
    for_sale: 'badge-success',
    pending: 'badge-warning',
    sold: 'badge-neutral',
    off_market: 'badge-ghost'
  }
  return colors[props.property.status] || 'badge-info'
})

const statusLabel = computed(() => {
  const labels: Record<string, string> = {
    for_sale: 'For Sale',
    pending: 'Pending',
    sold: 'Sold',
    off_market: 'Off Market'
  }
  return labels[props.property.status] || props.property.status
})

function handleClick() {
  emit('click')
}
</script>

<template>
  <div class="property-card" @click="handleClick">
    <!-- Image Container -->
    <div class="image-container">
      <img
        :src="primaryImage"
        :alt="property.full_street_line"
        class="property-image"
        loading="lazy"
      />
      
      <!-- Status Badge -->
      <div class="badge-container">
        <span class="badge" :class="statusBadgeColor">
          {{ statusLabel }}
        </span>
      </div>

      <!-- Favorite Button -->
      <div class="favorite-container">
        <FavoriteButton
          :property="property"
          size="md"
          variant="default"
        />
      </div>

      <!-- Image Overlay on Hover -->
      <div class="image-overlay">
        <svg class="overlay-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
        <p class="overlay-text">View Details</p>
      </div>
    </div>

    <!-- Content -->
    <div class="card-content">
      <!-- Price -->
      <div class="price">
        {{ formatPrice(property.list_price) }}
      </div>

      <!-- Details -->
      <div class="details">
        <span class="detail-item">{{ bedsAndBaths }}</span>
        <span v-if="squareFeet" class="detail-divider">•</span>
        <span v-if="squareFeet" class="detail-item">{{ squareFeet }}</span>
        <span v-if="property.price_per_sqft" class="detail-divider">•</span>
        <span v-if="property.price_per_sqft" class="detail-item">
          {{ formatPrice(property.price_per_sqft) }}/sqft
        </span>
      </div>

      <!-- Address -->
      <div class="address">
        <p class="street">{{ property.full_street_line }}</p>
        <p class="city">
          {{ property.city }}, {{ property.state }} {{ property.zip_code }}
        </p>
      </div>

      <!-- Property Type -->
      <div v-if="property.property_type" class="property-type">
        <svg class="type-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        <span class="type-label">{{ property.property_type.replace(/_/g, ' ') }}</span>
      </div>

      <!-- Days on Market (if available) -->
      <div v-if="property.days_on_mls" class="days-on-market">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ property.days_on_mls }} days on market
      </div>
    </div>
  </div>
</template>

<style scoped>
.property-card {
  @apply bg-white rounded-xl overflow-hidden shadow-md;
  @apply cursor-pointer;
  @apply transition-all duration-300;
  @apply hover:shadow-xl hover:-translate-y-1;
  border: 1px solid hsl(var(--b2));
}

/* Image Container */
.image-container {
  @apply relative w-full bg-base-300;
  padding-top: 66.67%; /* 3:2 aspect ratio */
  overflow: hidden;
}

.property-image {
  @apply absolute inset-0 w-full h-full object-cover;
  @apply transition-transform duration-500;
}

.property-card:hover .property-image {
  @apply scale-110;
}

/* Status Badge */
.badge-container {
  @apply absolute top-3 left-3 z-10;
}

.badge {
  @apply text-xs font-bold uppercase;
  @apply shadow-md;
}

/* Favorite Button */
.favorite-container {
  @apply absolute top-3 right-3 z-10;
}

/* Image Overlay */
.image-overlay {
  @apply absolute inset-0;
  @apply bg-black/60 backdrop-blur-sm;
  @apply flex flex-col items-center justify-center;
  @apply opacity-0 transition-all duration-300;
  @apply text-white;
  z-index: 5;
}

.property-card:hover .image-overlay {
  @apply opacity-100;
}

.overlay-icon {
  @apply w-12 h-12 mb-2;
  animation: pulse 2s ease-in-out infinite;
}

.overlay-text {
  @apply text-lg font-semibold;
}

/* Card Content */
.card-content {
  @apply p-5 space-y-3;
}

.price {
  @apply text-2xl font-bold text-primary;
  font-feature-settings: 'ss01', 'ss02';
}

.details {
  @apply flex items-center gap-2 text-sm text-base-content/70;
}

.detail-item {
  @apply font-medium;
}

.detail-divider {
  @apply text-base-content/30;
}

.address {
  @apply space-y-1;
}

.street {
  @apply font-semibold text-base-content;
  @apply truncate;
}

.city {
  @apply text-sm text-base-content/60;
}

.property-type {
  @apply flex items-center gap-2;
  @apply text-sm text-base-content/60;
  @apply pt-3 border-t border-base-200;
}

.type-icon {
  @apply w-4 h-4;
}

.type-label {
  @apply capitalize;
}

.days-on-market {
  @apply flex items-center gap-2;
  @apply text-xs text-base-content/50;
}

/* Animations */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .price {
    @apply text-xl;
  }
  
  .card-content {
    @apply p-4;
  }
}
</style>
