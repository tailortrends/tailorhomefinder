<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    count?: number
  }>(),
  {
    count: 6
  }
)

const skeletonArray = computed(() => Array.from({ length: props.count }))
</script>

<template>
  <div class="skeleton-grid">
    <div
      v-for="(_, index) in skeletonArray"
      :key="index"
      class="skeleton-card"
      :style="{ animationDelay: `${index * 0.05}s` }"
    >
      <!-- Image Skeleton -->
      <div class="skeleton-image" />

      <!-- Content Skeleton -->
      <div class="skeleton-content">
        <!-- Price -->
        <div class="skeleton-line h-8 w-36 mb-4" />

        <!-- Details -->
        <div class="skeleton-line h-5 w-full mb-3" />
        
        <!-- Address -->
        <div class="skeleton-line h-4 w-3/4 mb-2" />
        <div class="skeleton-line h-4 w-1/2 mb-4" />

        <!-- Features -->
        <div class="flex gap-2">
          <div class="skeleton-line h-6 w-20" />
          <div class="skeleton-line h-6 w-20" />
          <div class="skeleton-line h-6 w-20" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.skeleton-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6;
}

.skeleton-card {
  @apply bg-white rounded-xl overflow-hidden shadow-md;
  animation: fadeIn 0.5s ease-out forwards, shimmer 2s infinite;
  opacity: 0;
}

.skeleton-image {
  @apply w-full bg-gradient-to-r from-base-200 via-base-300 to-base-200;
  padding-top: 66.67%; /* 3:2 aspect ratio */
  position: relative;
  overflow: hidden;
}

.skeleton-image::before {
  content: '';
  @apply absolute inset-0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shimmerSlide 2s infinite;
}

.skeleton-content {
  @apply p-5;
}

.skeleton-line {
  @apply bg-base-200 rounded;
  position: relative;
  overflow: hidden;
}

.skeleton-line::before {
  content: '';
  @apply absolute inset-0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  animation: shimmerSlide 2s infinite;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes shimmer {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

@keyframes shimmerSlide {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style>
