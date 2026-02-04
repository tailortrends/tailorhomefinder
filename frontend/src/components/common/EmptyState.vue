<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    title?: string
    message?: string
    icon?: 'search' | 'home' | 'filter' | 'location'
    showAction?: boolean
    actionText?: string
  }>(),
  {
    title: 'No Properties Found',
    message: 'Try adjusting your filters or search in a different area.',
    icon: 'home',
    showAction: true,
    actionText: 'Reset Filters'
  }
)

const emit = defineEmits<{
  (e: 'action'): void
}>()

const iconPaths = {
  search: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z',
  home: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
  filter: 'M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z',
  location: 'M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z M15 11a3 3 0 11-6 0 3 3 0 016 0z'
}
</script>

<template>
  <div class="empty-state">
    <div class="empty-content">
      <!-- Animated Icon -->
      <div class="icon-container">
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
            :d="iconPaths[icon]"
          />
        </svg>
        
        <!-- Decorative circles -->
        <div class="circle circle-1" />
        <div class="circle circle-2" />
        <div class="circle circle-3" />
      </div>

      <!-- Text Content -->
      <h3 class="empty-title">{{ title }}</h3>
      <p class="empty-message">{{ message }}</p>

      <!-- Action Button -->
      <button
        v-if="showAction"
        class="btn btn-primary btn-lg mt-6"
        @click="emit('action')"
      >
        {{ actionText }}
      </button>

      <!-- Additional Suggestions -->
      <div class="suggestions">
        <p class="suggestions-title">Suggestions:</p>
        <ul class="suggestions-list">
          <li>Expand your search area</li>
          <li>Try different price ranges</li>
          <li>Adjust bedroom or bathroom requirements</li>
          <li>Remove property type restrictions</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.empty-state {
  @apply relative flex items-center justify-center py-20 px-4;
  @apply bg-gradient-to-br from-base-100 to-base-200;
  @apply rounded-2xl;
  min-height: 500px;
  overflow: hidden;
}

.empty-content {
  @apply relative z-10 flex flex-col items-center text-center max-w-lg;
}

/* Icon Animation */
.icon-container {
  @apply relative mb-8;
  width: 120px;
  height: 120px;
}

.empty-icon {
  @apply absolute inset-0 w-full h-full text-primary;
  animation: float 3s ease-in-out infinite;
}

.circle {
  @apply absolute rounded-full;
  @apply bg-primary/10;
}

.circle-1 {
  width: 140px;
  height: 140px;
  top: -10px;
  left: -10px;
  animation: pulse 2s ease-in-out infinite;
}

.circle-2 {
  width: 100px;
  height: 100px;
  top: 10px;
  left: 10px;
  animation: pulse 2s ease-in-out infinite 0.5s;
}

.circle-3 {
  width: 60px;
  height: 60px;
  top: 30px;
  left: 30px;
  animation: pulse 2s ease-in-out infinite 1s;
}

/* Text Styles */
.empty-title {
  @apply text-3xl font-bold text-base-content mb-3;
  font-feature-settings: 'ss01', 'ss02';
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

.empty-message {
  @apply text-lg text-base-content/70;
  animation: fadeInUp 0.6s ease-out 0.4s both;
}

/* Suggestions */
.suggestions {
  @apply mt-10 text-left w-full;
  animation: fadeInUp 0.6s ease-out 0.6s both;
}

.suggestions-title {
  @apply text-sm font-semibold text-base-content/80 mb-3;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.suggestions-list {
  @apply space-y-2;
}

.suggestions-list li {
  @apply text-sm text-base-content/60 pl-6 relative;
}

.suggestions-list li::before {
  content: '→';
  @apply absolute left-0 text-primary font-bold;
}

/* Animations */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.1;
  }
}

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

/* Background Pattern */
.empty-state::before {
  content: '';
  @apply absolute inset-0;
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(var(--p), 0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(var(--s), 0.05) 0%, transparent 50%);
  animation: backgroundShift 10s ease-in-out infinite;
}

@keyframes backgroundShift {
  0%, 100% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(20px, 20px);
  }
}
</style>
