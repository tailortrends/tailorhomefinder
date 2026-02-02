<template>
  <Transition name="slide-up">
    <div v-if="comparisonStore.comparisonList.length > 0" class="comparison-bar">
      <div class="container comparison-content">
        <div class="comparison-header">
          <div class="comparison-info">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 21h-6a4 4 0 0 1-4-4V5"/>
              <path d="M6 9h12a4 4 0 0 1 4 4v8"/>
              <path d="m6 9 3-3-3-3"/>
            </svg>
            <span class="comparison-count">
              {{ comparisonStore.comparisonList.length }} / {{ comparisonStore.maxComparisons }} Properties Selected
            </span>
          </div>
          <button class="btn-clear" @click="comparisonStore.clearComparison()">
            Clear All
          </button>
        </div>

        <div class="comparison-properties">
          <div 
            v-for="property in comparisonStore.comparisonList" 
            :key="property.id"
            class="comparison-item"
          >
            <img :src="property.image" :alt="property.title" />
            <div class="item-info">
              <span class="item-title">{{ property.title }}</span>
              <span class="item-price">{{ formatPrice(property.price) }}</span>
            </div>
            <button class="btn-remove" @click="comparisonStore.removeFromComparison(property.id)">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        </div>

        <button 
          v-if="comparisonStore.comparisonList.length >= 2"
          class="btn-compare"
          @click="$emit('open-comparison')"
        >
          Compare Properties
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14"/>
            <path d="m12 5 7 7-7 7"/>
          </svg>
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { useComparisonStore } from '@/stores/comparison'
import { formatPrice } from '@/utils/propertyHelpers'

const comparisonStore = useComparisonStore()

defineEmits<{
  openComparison: []
}>()
</script>

<style scoped>
.comparison-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #141414;
  border-top: 2px solid var(--color-gold-500);
  box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.5);
  z-index: 1000;
  padding: 1rem 0;
}

.comparison-content {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.comparison-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.comparison-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #fff;
  font-weight: 600;
}

.comparison-info svg {
  color: var(--color-gold-500);
}

.comparison-count {
  font-size: 0.9rem;
}

.btn-clear {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.375rem;
  color: #fff;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-clear:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
  color: #ef4444;
}

.comparison-properties {
  flex: 1;
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding: 0.5rem 0;
}

.comparison-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  min-width: 250px;
}

.comparison-item img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 0.375rem;
}

.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}

.item-title {
  color: #fff;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-price {
  color: var(--color-gold-500);
  font-size: 0.8rem;
  font-weight: 700;
}

.btn-remove {
  padding: 0.25rem;
  background: transparent;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  transition: color 0.2s;
}

.btn-remove:hover {
  color: #ef4444;
}

.btn-compare {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--color-gold-500);
  border: none;
  border-radius: 0.5rem;
  color: #000;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.btn-compare:hover {
  background: var(--color-gold-600);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
}
</style>