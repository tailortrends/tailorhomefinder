<script setup lang="ts">
import { computed } from 'vue'
import { useFavoritesStore } from '@/stores/favorites'
import type { Property } from '@/types/property'

const props = defineProps<{
  property: Property
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
  variant?: 'default' | 'minimal' | 'outline'
}>()

const favoritesStore = useFavoritesStore()

const isFavorited = computed(() => 
  favoritesStore.isFavorited(props.property.property_id)
)

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'w-5 h-5',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  }
  return sizes[props.size || 'md']
})

const buttonClasses = computed(() => {
  const base = 'favorite-btn'
  const variants = {
    default: 'btn-circle',
    minimal: 'btn-ghost btn-circle',
    outline: 'btn-outline btn-circle'
  }
  return `${base} ${variants[props.variant || 'default']}`
})

async function handleToggle(event: Event) {
  event.preventDefault()
  event.stopPropagation()
  
  await favoritesStore.toggleFavorite(props.property)
}
</script>

<template>
  <button
    :class="[buttonClasses, { 'favorited': isFavorited }]"
    :aria-label="isFavorited ? 'Remove from favorites' : 'Add to favorites'"
    @click="handleToggle"
  >
    <!-- Heart Icon -->
    <svg
      :class="sizeClasses"
      class="heart-icon"
      :fill="isFavorited ? 'currentColor' : 'none'"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
      />
    </svg>

    <!-- Optional Label -->
    <span v-if="showLabel" class="favorite-label">
      {{ isFavorited ? 'Saved' : 'Save' }}
    </span>
  </button>
</template>

<style scoped>
.favorite-btn {
  @apply relative;
  @apply transition-all duration-300;
  @apply hover:scale-110;
}

.favorite-btn:not(.favorited) {
  @apply bg-white/90 backdrop-blur-sm;
  @apply text-base-content;
  @apply border-2 border-base-300;
}

.favorite-btn:not(.favorited):hover {
  @apply bg-white border-error text-error;
}

.favorite-btn.favorited {
  @apply bg-error text-white;
  @apply border-2 border-error;
  animation: heartBeat 0.3s ease-out;
}

.favorite-btn.favorited:hover {
  @apply bg-error/80;
}

.heart-icon {
  @apply transition-all duration-300;
}

.favorite-btn.favorited .heart-icon {
  animation: heartPulse 0.5s ease-out;
}

.favorite-label {
  @apply ml-2 text-sm font-medium;
}

/* Animations */
@keyframes heartBeat {
  0% {
    transform: scale(1);
  }
  25% {
    transform: scale(1.3);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes heartPulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

/* Loading state */
.favorite-btn:disabled {
  @apply opacity-50 cursor-not-allowed;
  animation: none;
}

.favorite-btn:disabled:hover {
  transform: none;
}

/* Ripple effect on click */
.favorite-btn::before {
  content: '';
  @apply absolute inset-0 rounded-full;
  @apply bg-error/20;
  @apply scale-0 opacity-0;
  @apply transition-all duration-300;
}

.favorite-btn:active::before {
  @apply scale-150 opacity-100;
  transition: all 0.2s ease-out;
}
</style>
