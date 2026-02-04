<script setup lang="ts">
import { ref, computed } from 'vue'
import type { PropertyFilters } from '@/types/property'

const emit = defineEmits<{
  (e: 'update:filters', filters: PropertyFilters): void
  (e: 'search'): void
}>()

const props = defineProps<{
  filters: PropertyFilters
}>()

// Local state for form inputs
const localFilters = ref<PropertyFilters>({ ...props.filters })

// Price ranges
const priceRanges = [
  { label: 'Any Price', min: undefined, max: undefined },
  { label: '$0 - $500k', min: 0, max: 500000 },
  { label: '$500k - $1M', min: 500000, max: 1000000 },
  { label: '$1M - $2M', min: 1000000, max: 2000000 },
  { label: '$2M - $5M', min: 2000000, max: 5000000 },
  { label: '$5M+', min: 5000000, max: undefined }
]

const bedroomOptions = [
  { label: 'Any', value: undefined },
  { label: '1+', value: 1 },
  { label: '2+', value: 2 },
  { label: '3+', value: 3 },
  { label: '4+', value: 4 },
  { label: '5+', value: 5 }
]

const bathroomOptions = [
  { label: 'Any', value: undefined },
  { label: '1+', value: 1 },
  { label: '2+', value: 2 },
  { label: '3+', value: 3 },
  { label: '4+', value: 4 }
]

const propertyTypes = [
  { label: 'All Types', value: undefined },
  { label: 'Single Family', value: 'single_family_residential' },
  { label: 'Condo', value: 'condo' },
  { label: 'Townhouse', value: 'townhouse' },
  { label: 'Multi-Family', value: 'multi_family' },
  { label: 'Land', value: 'land' }
]

const showAdvanced = ref(false)

const activeFilterCount = computed(() => {
  let count = 0
  if (localFilters.value.minPrice || localFilters.value.maxPrice) count++
  if (localFilters.value.minBeds) count++
  if (localFilters.value.minBaths) count++
  if (localFilters.value.propertyType) count++
  if (localFilters.value.minSqft || localFilters.value.maxSqft) count++
  return count
})

function applyFilters() {
  emit('update:filters', { ...localFilters.value })
  emit('search')
}

function resetFilters() {
  localFilters.value = {
    location: localFilters.value.location,
    minPrice: undefined,
    maxPrice: undefined,
    minBeds: undefined,
    minBaths: undefined,
    propertyType: undefined,
    minSqft: undefined,
    maxSqft: undefined
  }
  applyFilters()
}

function setPriceRange(range: { min?: number; max?: number }) {
  localFilters.value.minPrice = range.min
  localFilters.value.maxPrice = range.max
}
</script>

<template>
  <div class="search-filters">
    <!-- Main Filter Bar -->
    <div class="filter-bar">
      <!-- Location Input -->
      <div class="filter-group location-group">
        <label class="filter-label">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Location
        </label>
        <input
          v-model="localFilters.location"
          type="text"
          placeholder="City, ZIP, or Address"
          class="input input-bordered w-full"
          @keyup.enter="applyFilters"
        />
      </div>

      <!-- Price Range Dropdown -->
      <div class="filter-group">
        <label class="filter-label">Price Range</label>
        <select
          class="select select-bordered w-full"
          @change="(e) => setPriceRange(priceRanges[(e.target as HTMLSelectElement).selectedIndex])"
        >
          <option
            v-for="range in priceRanges"
            :key="range.label"
            :selected="range.min === localFilters.minPrice && range.max === localFilters.maxPrice"
          >
            {{ range.label }}
          </option>
        </select>
      </div>

      <!-- Bedrooms -->
      <div class="filter-group">
        <label class="filter-label">Beds</label>
        <select v-model="localFilters.minBeds" class="select select-bordered w-full">
          <option v-for="opt in bedroomOptions" :key="opt.label" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </div>

      <!-- Bathrooms -->
      <div class="filter-group">
        <label class="filter-label">Baths</label>
        <select v-model="localFilters.minBaths" class="select select-bordered w-full">
          <option v-for="opt in bathroomOptions" :key="opt.label" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </div>

      <!-- Property Type -->
      <div class="filter-group">
        <label class="filter-label">Property Type</label>
        <select v-model="localFilters.propertyType" class="select select-bordered w-full">
          <option v-for="type in propertyTypes" :key="type.label" :value="type.value">
            {{ type.label }}
          </option>
        </select>
      </div>

      <!-- Search Button -->
      <div class="filter-actions">
        <button class="btn btn-primary search-btn" @click="applyFilters">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          Search
        </button>
        
        <button 
          v-if="activeFilterCount > 0"
          class="btn btn-ghost btn-sm"
          @click="resetFilters"
        >
          Reset ({{ activeFilterCount }})
        </button>
      </div>
    </div>

    <!-- Advanced Filters Toggle -->
    <div class="advanced-toggle">
      <button
        class="btn btn-ghost btn-sm gap-2"
        @click="showAdvanced = !showAdvanced"
      >
        <svg
          class="w-4 h-4 transition-transform"
          :class="{ 'rotate-180': showAdvanced }"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
        {{ showAdvanced ? 'Hide' : 'Show' }} Advanced Filters
      </button>
    </div>

    <!-- Advanced Filters Panel -->
    <Transition name="slide-fade">
      <div v-if="showAdvanced" class="advanced-panel">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Min Square Feet -->
          <div class="form-control">
            <label class="label">
              <span class="label-text">Min Square Feet</span>
            </label>
            <input
              v-model.number="localFilters.minSqft"
              type="number"
              placeholder="e.g., 1500"
              class="input input-bordered"
              min="0"
              step="100"
            />
          </div>

          <!-- Max Square Feet -->
          <div class="form-control">
            <label class="label">
              <span class="label-text">Max Square Feet</span>
            </label>
            <input
              v-model.number="localFilters.maxSqft"
              type="number"
              placeholder="e.g., 5000"
              class="input input-bordered"
              min="0"
              step="100"
            />
          </div>

          <!-- Custom Price Min -->
          <div class="form-control">
            <label class="label">
              <span class="label-text">Min Price ($)</span>
            </label>
            <input
              v-model.number="localFilters.minPrice"
              type="number"
              placeholder="e.g., 500000"
              class="input input-bordered"
              min="0"
              step="10000"
            />
          </div>

          <!-- Custom Price Max -->
          <div class="form-control">
            <label class="label">
              <span class="label-text">Max Price ($)</span>
            </label>
            <input
              v-model.number="localFilters.maxPrice"
              type="number"
              placeholder="e.g., 2000000"
              class="input input-bordered"
              min="0"
              step="10000"
            />
          </div>
        </div>

        <div class="flex justify-end gap-2 mt-4">
          <button class="btn btn-ghost" @click="showAdvanced = false">
            Close
          </button>
          <button class="btn btn-primary" @click="applyFilters">
            Apply Advanced Filters
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.search-filters {
  @apply bg-white rounded-xl shadow-lg p-6 mb-6;
  border: 1px solid hsl(var(--b2));
}

.filter-bar {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4 items-end;
}

.filter-group {
  @apply flex flex-col gap-2;
}

.location-group {
  @apply lg:col-span-2;
}

.filter-label {
  @apply text-sm font-medium text-base-content/70 flex items-center gap-2;
}

.icon {
  @apply w-4 h-4;
}

.filter-actions {
  @apply flex flex-col gap-2;
}

.search-btn {
  @apply gap-2 font-semibold;
}

.advanced-toggle {
  @apply mt-4 pt-4 border-t border-base-200;
}

.advanced-panel {
  @apply mt-4 p-4 bg-base-100 rounded-lg;
  border: 1px solid hsl(var(--b2));
}

/* Transitions */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .filter-bar {
    @apply grid-cols-1;
  }
  
  .filter-actions {
    @apply flex-row;
  }
}
</style>
