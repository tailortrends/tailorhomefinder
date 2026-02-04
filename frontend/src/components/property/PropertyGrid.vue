<script setup lang="ts">
import { computed } from 'vue'
import type { Property } from '@/types/property'
import PropertyCard from './PropertyCard.vue'

const props = defineProps<{
  properties: Property[]
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'property-click', property: Property): void
}>()

const gridClass = computed(() => {
  const count = props.properties.length
  if (count === 0) return 'grid-cols-1'
  if (count === 1) return 'grid-cols-1 lg:grid-cols-1'
  if (count === 2) return 'grid-cols-1 md:grid-cols-2'
  return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
})

function handlePropertyClick(property: Property) {
  emit('property-click', property)
}
</script>

<template>
  <div class="property-grid">
    <!-- Results Header -->
    <div v-if="!loading && properties.length > 0" class="results-header">
      <h2 class="results-count">
        {{ properties.length }} {{ properties.length === 1 ? 'Property' : 'Properties' }} Found
      </h2>
    </div>

    <!-- Property Grid -->
    <div
      v-if="!loading && properties.length > 0"
      class="grid gap-6"
      :class="gridClass"
    >
      <PropertyCard
        v-for="property in properties"
        :key="property.property_id"
        :property="property"
        @click="handlePropertyClick(property)"
      />
    </div>

    <!-- Loading Skeletons -->
    <div
      v-if="loading"
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <div
        v-for="i in 6"
        :key="i"
        class="skeleton-card"
      >
        <div class="skeleton-image" />
        <div class="skeleton-content">
          <div class="skeleton-line h-6 w-32 mb-3" />
          <div class="skeleton-line h-4 w-48 mb-2" />
          <div class="skeleton-line h-4 w-full mb-2" />
          <div class="skeleton-line h-4 w-3/4" />
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-if="!loading && properties.length === 0"
      class="empty-state"
    >
      <svg
        class="empty-icon"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
        />
      </svg>
      <h3 class="empty-title">No Properties Found</h3>
      <p class="empty-message">
        Try adjusting your filters or search in a different area.
      </p>
    </div>
  </div>
</template>

<style scoped>
.property-grid {
  @apply w-full;
}

.results-header {
  @apply mb-6;
}

.results-count {
  @apply text-2xl font-bold text-base-content;
  font-feature-settings: 'ss01', 'ss02';
}

/* Loading Skeletons */
.skeleton-card {
  @apply bg-white rounded-xl overflow-hidden shadow-md;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.skeleton-image {
  @apply w-full bg-base-200;
  padding-top: 66.67%; /* 3:2 aspect ratio */
}

.skeleton-content {
  @apply p-4;
}

.skeleton-line {
  @apply bg-base-200 rounded;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Empty State */
.empty-state {
  @apply flex flex-col items-center justify-center py-20 px-4;
  @apply bg-base-100 rounded-xl border-2 border-dashed border-base-300;
}

.empty-icon {
  @apply w-24 h-24 text-base-300 mb-6;
}

.empty-title {
  @apply text-2xl font-bold text-base-content mb-2;
}

.empty-message {
  @apply text-base-content/60 text-center max-w-md;
}

/* Grid Animations */
.grid > * {
  animation: fadeInUp 0.5s ease-out forwards;
  opacity: 0;
}

.grid > *:nth-child(1) { animation-delay: 0.05s; }
.grid > *:nth-child(2) { animation-delay: 0.1s; }
.grid > *:nth-child(3) { animation-delay: 0.15s; }
.grid > *:nth-child(4) { animation-delay: 0.2s; }
.grid > *:nth-child(5) { animation-delay: 0.25s; }
.grid > *:nth-child(6) { animation-delay: 0.3s; }

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
</style>
