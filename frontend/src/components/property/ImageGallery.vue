<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  images: string[]
  propertyTitle?: string
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const currentIndex = ref(0)
const showLightbox = ref(false)
const isTransitioning = ref(false)

const currentImage = computed(() => props.images[currentIndex.value] || '')
const hasMultipleImages = computed(() => props.images.length > 1)

const thumbnailsToShow = computed(() => {
  if (props.images.length <= 5) return props.images
  
  const start = Math.max(0, currentIndex.value - 2)
  const end = Math.min(props.images.length, start + 5)
  return props.images.slice(start, end)
})

function openLightbox(index: number) {
  currentIndex.value = index
  showLightbox.value = true
  document.body.style.overflow = 'hidden'
}

function closeLightbox() {
  showLightbox.value = false
  document.body.style.overflow = ''
  emit('close')
}

function nextImage() {
  if (isTransitioning.value) return
  isTransitioning.value = true
  
  currentIndex.value = (currentIndex.value + 1) % props.images.length
  
  setTimeout(() => {
    isTransitioning.value = false
  }, 300)
}

function prevImage() {
  if (isTransitioning.value) return
  isTransitioning.value = true
  
  currentIndex.value = currentIndex.value === 0 
    ? props.images.length - 1 
    : currentIndex.value - 1
  
  setTimeout(() => {
    isTransitioning.value = false
  }, 300)
}

function goToImage(index: number) {
  if (isTransitioning.value) return
  isTransitioning.value = true
  currentIndex.value = index
  
  setTimeout(() => {
    isTransitioning.value = false
  }, 300)
}

// Keyboard navigation
function handleKeydown(e: KeyboardEvent) {
  if (!showLightbox.value) return
  
  if (e.key === 'ArrowRight') nextImage()
  if (e.key === 'ArrowLeft') prevImage()
  if (e.key === 'Escape') closeLightbox()
}

// Mount keyboard listeners
if (typeof window !== 'undefined') {
  window.addEventListener('keydown', handleKeydown)
}
</script>

<template>
  <div class="image-gallery">
    <!-- Main Image Display -->
    <div class="gallery-main">
      <div class="main-image-container" @click="openLightbox(0)">
        <img
          :src="currentImage"
          :alt="`${propertyTitle} - Main view`"
          class="main-image"
        />
        
        <!-- View All Photos Button -->
        <button class="view-all-btn">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          View All {{ images.length }} Photos
        </button>

        <!-- Navigation Arrows -->
        <button
          v-if="hasMultipleImages"
          class="nav-arrow nav-arrow-left"
          @click.stop="prevImage"
        >
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <button
          v-if="hasMultipleImages"
          class="nav-arrow nav-arrow-right"
          @click.stop="nextImage"
        >
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- Image Counter -->
      <div class="image-counter">
        {{ currentIndex + 1 }} / {{ images.length }}
      </div>
    </div>

    <!-- Thumbnail Grid -->
    <div v-if="images.length > 1" class="thumbnail-grid">
      <button
        v-for="(image, index) in thumbnailsToShow"
        :key="index"
        class="thumbnail"
        :class="{ 'thumbnail-active': index === currentIndex }"
        @click="goToImage(index)"
      >
        <img :src="image" :alt="`Thumbnail ${index + 1}`" />
      </button>
    </div>

    <!-- Lightbox Modal -->
    <Teleport to="body">
      <Transition name="lightbox-fade">
        <div
          v-if="showLightbox"
          class="lightbox-overlay"
          @click.self="closeLightbox"
        >
          <!-- Close Button -->
          <button class="lightbox-close" @click="closeLightbox">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- Main Image -->
          <div class="lightbox-content">
            <Transition :name="'slide'" mode="out-in">
              <img
                :key="currentIndex"
                :src="currentImage"
                :alt="`${propertyTitle} - Image ${currentIndex + 1}`"
                class="lightbox-image"
              />
            </Transition>
          </div>

          <!-- Navigation -->
          <button
            v-if="hasMultipleImages"
            class="lightbox-nav lightbox-nav-left"
            @click="prevImage"
          >
            <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          
          <button
            v-if="hasMultipleImages"
            class="lightbox-nav lightbox-nav-right"
            @click="nextImage"
          >
            <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>

          <!-- Counter -->
          <div class="lightbox-counter">
            {{ currentIndex + 1 }} / {{ images.length }}
          </div>

          <!-- Thumbnail Strip -->
          <div class="lightbox-thumbnails">
            <button
              v-for="(image, index) in images"
              :key="index"
              class="lightbox-thumbnail"
              :class="{ 'lightbox-thumbnail-active': index === currentIndex }"
              @click="goToImage(index)"
            >
              <img :src="image" :alt="`Thumbnail ${index + 1}`" />
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.image-gallery {
  @apply w-full;
}

/* Main Gallery */
.gallery-main {
  @apply relative mb-4;
}

.main-image-container {
  @apply relative rounded-2xl overflow-hidden cursor-pointer;
  @apply bg-base-300;
  aspect-ratio: 16 / 9;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.main-image {
  @apply w-full h-full object-cover;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.main-image-container:hover .main-image {
  transform: scale(1.05);
}

/* View All Button */
.view-all-btn {
  @apply absolute bottom-6 right-6;
  @apply bg-white text-base-content;
  @apply px-6 py-3 rounded-xl;
  @apply font-semibold;
  @apply flex items-center gap-2;
  @apply shadow-lg;
  @apply transition-all duration-300;
  z-index: 10;
}

.view-all-btn:hover {
  @apply bg-primary text-white scale-105;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

/* Navigation Arrows */
.nav-arrow {
  @apply absolute top-1/2 -translate-y-1/2;
  @apply bg-white/90 backdrop-blur-sm;
  @apply text-base-content;
  @apply p-3 rounded-full;
  @apply shadow-lg;
  @apply opacity-0 transition-all duration-300;
  z-index: 10;
}

.main-image-container:hover .nav-arrow {
  @apply opacity-100;
}

.nav-arrow-left {
  @apply left-4;
}

.nav-arrow-right {
  @apply right-4;
}

.nav-arrow:hover {
  @apply bg-white scale-110;
}

/* Image Counter */
.image-counter {
  @apply absolute top-6 left-6;
  @apply bg-black/60 backdrop-blur-sm;
  @apply text-white px-4 py-2 rounded-lg;
  @apply text-sm font-medium;
  z-index: 10;
}

/* Thumbnail Grid */
.thumbnail-grid {
  @apply grid grid-cols-5 gap-3;
}

.thumbnail {
  @apply relative rounded-lg overflow-hidden;
  @apply border-3 border-transparent;
  @apply transition-all duration-300;
  aspect-ratio: 4 / 3;
}

.thumbnail img {
  @apply w-full h-full object-cover;
}

.thumbnail:hover {
  @apply border-primary scale-105;
}

.thumbnail-active {
  @apply border-primary ring-2 ring-primary ring-offset-2;
}

/* Lightbox */
.lightbox-overlay {
  @apply fixed inset-0 z-50;
  @apply bg-black/95 backdrop-blur-md;
  @apply flex items-center justify-center;
  @apply p-4;
}

.lightbox-close {
  @apply absolute top-6 right-6;
  @apply text-white hover:text-primary;
  @apply p-2 rounded-full;
  @apply transition-all duration-300;
  @apply hover:bg-white/10;
  z-index: 60;
}

.lightbox-content {
  @apply relative max-w-7xl max-h-[85vh] mx-auto;
  @apply flex items-center justify-center;
}

.lightbox-image {
  @apply max-w-full max-h-[85vh] object-contain;
  @apply rounded-lg shadow-2xl;
}

.lightbox-nav {
  @apply absolute top-1/2 -translate-y-1/2;
  @apply text-white hover:text-primary;
  @apply p-4 rounded-full;
  @apply transition-all duration-300;
  @apply hover:bg-white/10;
  z-index: 60;
}

.lightbox-nav-left {
  @apply left-6;
}

.lightbox-nav-right {
  @apply right-6;
}

.lightbox-counter {
  @apply absolute top-6 left-1/2 -translate-x-1/2;
  @apply bg-white/20 backdrop-blur-sm;
  @apply text-white px-6 py-3 rounded-full;
  @apply font-medium;
  z-index: 60;
}

/* Lightbox Thumbnails */
.lightbox-thumbnails {
  @apply absolute bottom-6 left-1/2 -translate-x-1/2;
  @apply flex gap-2 overflow-x-auto;
  @apply max-w-[90vw] px-4;
  z-index: 60;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.lightbox-thumbnail {
  @apply flex-shrink-0 w-20 h-20;
  @apply rounded-lg overflow-hidden;
  @apply border-2 border-transparent;
  @apply transition-all duration-300;
  @apply hover:border-white hover:scale-110;
}

.lightbox-thumbnail img {
  @apply w-full h-full object-cover;
}

.lightbox-thumbnail-active {
  @apply border-primary ring-2 ring-primary;
}

/* Animations */
.lightbox-fade-enter-active,
.lightbox-fade-leave-active {
  transition: opacity 0.3s ease;
}

.lightbox-fade-enter-from,
.lightbox-fade-leave-to {
  opacity: 0;
}

.slide-enter-active {
  transition: all 0.3s ease-out;
}

.slide-leave-active {
  transition: all 0.3s ease-in;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Responsive */
@media (max-width: 768px) {
  .thumbnail-grid {
    @apply grid-cols-4;
  }
  
  .lightbox-thumbnails {
    @apply bottom-2 gap-1;
  }
  
  .lightbox-thumbnail {
    @apply w-16 h-16;
  }
  
  .nav-arrow {
    @apply p-2;
  }
}
</style>
