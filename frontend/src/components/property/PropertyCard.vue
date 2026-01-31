<template>
  <div 
    class="property-card group"
    @click="$emit('select', property)"
  >
    <!-- Image -->
    <div class="property-image">
      <img 
        :src="property.image" 
        :alt="property.title"
      />
      <div class="image-overlay" />
      
      <!-- Status Badge -->
      <div class="badges">
        <span class="badge badge-type">{{ property.type }}</span>
        <span 
          v-if="property.status" 
          :class="['badge', `badge-${property.status?.toLowerCase()}`]"
        >
          {{ property.status }}
        </span>
      </div>

      <!-- Favorite Button -->
      <button 
        class="favorite-btn"
        @click.stop="toggleFavorite"
      >
        <svg 
          class="heart-icon"
          :class="{ 'filled': isFavorite }"
          xmlns="http://www.w3.org/2000/svg" 
          width="16" 
          height="16" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="2" 
          stroke-linecap="round" 
          stroke-linejoin="round"
        >
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
      </button>
    </div>

    <!-- Content -->
    <div class="property-content">
      <div class="property-header">
        <h3 class="property-title">{{ property.title }}</h3>
        <div class="property-location">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          {{ property.location }}
        </div>
      </div>

      <!-- Stats -->
      <div class="property-stats">
        <div class="stat">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9h18v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9Z"/>
            <path d="M3 9V7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v2"/>
          </svg>
          <span>{{ property.beds || '-' }}</span>
        </div>
        <div class="stat">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-1 0l-1 1a1.5 1.5 0 0 0 0 1L7 9"/>
            <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
          </svg>
          <span>{{ property.baths || '-' }}</span>
        </div>
        <div class="stat">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15V6"/>
            <path d="M18.5 18a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z"/>
            <path d="M12 12H3"/>
            <path d="M16 6H3"/>
            <path d="M12 18H3"/>
          </svg>
          <span>{{ formatSqft(property.sqft) }}</span>
        </div>
        <div class="stat">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect width="18" height="18" x="3" y="3" rx="2"/>
            <path d="M3 9h18"/>
            <path d="M9 21V9"/>
          </svg>
          <span>{{ property.yearBuilt || '-' }}</span>
        </div>
      </div>

      <!-- Price & CTA -->
      <div class="property-footer">
        <span class="property-price">{{ formatPrice(property.price) }}</span>
        <span class="view-details">
          View Details
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14"/>
            <path d="m12 5 7 7-7 7"/>
          </svg>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { Property } from '@/types/property';
import { formatPrice, formatSqft } from '@/utils/propertyHelpers';

interface Props {
  property: Property;
}

const props = defineProps<Props>();

defineEmits<{
  select: [property: Property];
}>();

const isFavorite = ref(false);

const toggleFavorite = () => {
  isFavorite.value = !isFavorite.value;
  
  try {
    const saved = localStorage.getItem('tailor_favorites');
    let favorites: string[] = saved ? JSON.parse(saved) : [];
    
    if (!Array.isArray(favorites)) favorites = [];

    if (isFavorite.value) {
      if (!favorites.includes(props.property.id)) {
        favorites.push(props.property.id);
      }
    } else {
      favorites = favorites.filter(id => id !== props.property.id);
    }
    
    localStorage.setItem('tailor_favorites', JSON.stringify(favorites));
  } catch (e) {
    console.error('Error saving favorite:', e);
  }
};

onMounted(() => {
  try {
    const saved = localStorage.getItem('tailor_favorites');
    const favorites = saved ? JSON.parse(saved) : [];
    isFavorite.value = Array.isArray(favorites) && favorites.includes(props.property.id);
  } catch (e) {
    console.error('Error loading favorites:', e);
  }
});
</script>

<style scoped>
.property-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.property-card:hover {
  border-color: var(--color-gold-500);
  box-shadow: 0 0 30px rgba(212, 175, 55, 0.1);
  transform: translateY(-2px);
}

.property-image {
  position: relative;
  aspect-ratio: 4 / 3;
  overflow: hidden;
}

.property-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.7s ease;
}

.property-card:hover .property-image img {
  transform: scale(1.1);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.6), transparent);
  opacity: 0.6;
}

.badges {
  position: absolute;
  top: 1rem;
  left: 1rem;
  display: flex;
  gap: 0.5rem;
  z-index: 10;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  backdrop-filter: blur(8px);
}

.badge-type {
  background: rgba(255, 255, 255, 0.9);
  color: var(--color-gold-600);
  border: 1px solid rgba(212, 175, 55, 0.2);
}

.badge-active {
  background: rgba(16, 185, 129, 0.9);
  color: white;
}

.badge-pending {
  background: rgba(245, 158, 11, 0.9);
  color: white;
}

.badge-sold {
  background: rgba(107, 114, 128, 0.9);
  color: white;
}

.favorite-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 10;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid transparent;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
}

.favorite-btn:hover {
  background: var(--color-gold-500);
  transform: scale(1.1);
}

.heart-icon {
  display: block;
  color: var(--color-text);
  transition: all 0.3s ease;
}

.heart-icon.filled {
  fill: var(--color-gold-500);
  stroke: var(--color-gold-500);
}

.property-content {
  padding: 1.5rem;
}

.property-header {
  margin-bottom: 1rem;
}

.property-title {
  font-family: var(--font-family-serif);
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 0.25rem;
  transition: color 0.3s ease;
}

.property-card:hover .property-title {
  color: var(--color-gold-500);
}

.property-location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.property-location svg {
  color: var(--color-gold-500);
  flex-shrink: 0;
}

.property-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  padding: 1rem 0;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 1rem;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  text-align: center;
}

.stat svg {
  color: var(--color-text-secondary);
}

.stat span {
  font-family: var(--font-family-display);
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text);
}

.property-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.property-price {
  font-family: var(--font-family-display);
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-text);
}

.view-details {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-gold-500);
  font-size: var(--font-size-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  transition: all 0.3s ease;
}

.property-card:hover .view-details {
  transform: translateX(4px);
}

@media (prefers-color-scheme: dark) {
  .badge-type {
    background: rgba(0, 0, 0, 0.6);
    color: var(--color-gold-400);
  }
  
  .favorite-btn {
    background: rgba(0, 0, 0, 0.6);
  }
}
</style>