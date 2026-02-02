<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click.self="close">
        <div class="modal-container">
          <div class="modal-header">
            <h2>Property Comparison</h2>
            <button class="btn-close" @click="close">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <div class="comparison-table-wrapper">
              <table class="comparison-table">
                <thead>
                  <tr>
                    <th class="feature-col">Feature</th>
                    <th v-for="property in properties" :key="property.id" class="property-col">
                      <div class="property-header-cell">
                        <img :src="property.image" :alt="property.title" />
                        <h3>{{ property.title }}</h3>
                        <p class="location">{{ property.location }}</p>
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <!-- Price -->
                  <tr>
                    <td class="feature-name">Price</td>
                    <td v-for="property in properties" :key="property.id" class="value-cell">
                      <span class="price-value">{{ formatPrice(property.price) }}</span>
                    </td>
                  </tr>

                  <!-- Bedrooms -->
                  <tr>
                    <td class="feature-name">Bedrooms</td>
                    <td v-for="property in properties" :key="property.id" class="value-cell">
                      {{ property.beds || '-' }}
                    </td>
                  </tr>

                  <!-- Bathrooms -->
                  <tr>
                    <td class="feature-name">Bathrooms</td>
                    <td v-for="property in properties" :key="property.id" class="value-cell">
                      {{ property.baths || '-' }}
                    </td>
                  </tr>

                  <!-- Square Feet -->
                  <tr>
                    <td class="feature-name">Square Feet</td>
                    <td v-for="property in properties" :key="property.id" class="value-cell">
                      {{ property.sqft?.toLocaleString() || '-' }}
                    </td>
                  </tr>

                  <!-- Year Built -->
                  <tr>
                    <td class="feature-name">Year Built</td>
                    <td v-for="property in properties" :key="property.id" class="value-cell">
                      {{ property.yearBuilt || '-' }}
                    </td>
                  </tr>

                  <!-- Property Type -->
                  <tr>
                    <td class="feature-name">Property Type</td>
                    <td v-for="property in properties" :key="property.id" class="value-cell">
                      {{ property.type }}
                    </td>
                  </tr>

                  <!-- Status -->
                  <tr>
                    <td class="feature-name">Status</td>
                    <td v-for="property in properties" :key="property.id" class="value-cell">
                      <span :class="['status-badge', `status-${property.status?.toLowerCase()}`]">
                        {{ property.status || 'N/A' }}
                      </span>
                    </td>
                  </tr>

                  <!-- Lot Size -->
                  <tr>
                    <td class="feature-name">Lot Size</td>
                    <td v-for="property in properties" :key="property.id" class="value-cell">
                      {{ property.lotSqft ? property.lotSqft.toLocaleString() + ' sq ft' : '-' }}
                    </td>
                  </tr>

                  <!-- HOA Fee -->
                  <tr>
                    <td class="feature-name">HOA Fee</td>
                    <td v-for="property in properties" :key="property.id" class="value-cell">
                      {{ property.hoaFee ? '$' + property.hoaFee + '/mo' : '-' }}
                    </td>
                  </tr>

                  <!-- Price per Sq Ft -->
                  <tr>
                    <td class="feature-name">Price per Sq Ft</td>
                    <td v-for="property in properties" :key="property.id" class="value-cell">
                      {{ calculatePricePerSqft(property) }}
                    </td>
                  </tr>

                  <!-- Actions -->
                  <tr class="action-row">
                    <td class="feature-name"></td>
                    <td v-for="property in properties" :key="property.id" class="action-cell">
                      <button class="btn-view" @click="viewProperty(property.id)">
                        View Details
                      </button>
                      <button class="btn-remove-modal" @click="removeProperty(property.id)">
                        Remove
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import type { Property } from '@/types/property'
import { formatPrice } from '@/utils/propertyHelpers'
import { useComparisonStore } from '@/stores/comparison'

interface Props {
  isOpen: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  close: []
}>()

const router = useRouter()
const comparisonStore = useComparisonStore()

const properties = computed(() => comparisonStore.comparisonList)

const close = () => {
  emit('close')
}

const calculatePricePerSqft = (property: Property) => {
  if (!property.sqft || property.sqft === 0) return '-'
  const pricePerSqft = property.price / property.sqft
  return '$' + pricePerSqft.toFixed(0)
}

const viewProperty = (propertyId: string) => {
  close()
  router.push({ name: 'property-detail', params: { id: propertyId } })
}

const removeProperty = (propertyId: string) => {
  comparisonStore.removeFromComparison(propertyId)
  if (comparisonStore.comparisonList.length < 2) {
    close()
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 9999;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 2rem;
  padding-top: 2rem;
  padding-bottom: 140px;
  overflow-y: auto;
}

.modal-container {
  background: #0c0c0c;
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 1rem;
  width: 100%;
  max-width: 1400px;
  max-height: calc(90vh - 120px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  margin-bottom: 120px;
  margin-top: 0;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h2 {
  font-family: Georgia, serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-gold-500);
}

.btn-close {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-close:hover {
  background: var(--color-gold-500);
  border-color: var(--color-gold-600);
  transform: scale(1.1);
}

.modal-body {
  flex: 1;
  overflow: auto;
  padding: 2rem;
  padding-bottom: 3rem;
}

.comparison-table-wrapper {
  overflow-x: auto;
}

.comparison-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  table-layout: fixed;
}

.comparison-table thead th {
  background: #141414;
  position: sticky;
  top: 0;
  z-index: 10;
  padding: 1.5rem 1rem;
  border-bottom: 2px solid var(--color-gold-500);
  vertical-align: top;
}

.feature-col {
  text-align: left;
  font-size: 0.85rem;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  width: 180px;
  min-width: 180px;
  vertical-align: top;
}

.property-col {
  width: 300px;
  min-width: 300px;
  vertical-align: top;
}

.property-header-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.property-header-cell img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.property-header-cell h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
  text-align: center;
}

.property-header-cell .location {
  font-size: 0.85rem;
  color: #9ca3af;
  text-align: center;
}

.comparison-table tbody tr {
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.comparison-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.02);
}

.comparison-table tbody td {
  vertical-align: top;
}

.feature-name {
  padding: 1.25rem 1rem;
  font-weight: 600;
  color: #d1d5db;
  font-size: 0.9rem;
  vertical-align: top;
}

.value-cell {
  padding: 1.25rem 1rem;
  text-align: center;
  color: #fff;
  font-size: 0.95rem;
  vertical-align: top;
}

.price-value {
  font-family: Georgia, serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-gold-500);
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-active {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.status-pending {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.status-sold {
  background: rgba(107, 114, 128, 0.2);
  color: #6b7280;
}

.action-row {
  background: rgba(255, 255, 255, 0.02);
}

.action-cell {
  padding: 1.5rem 1rem;
  vertical-align: top;
}

.btn-view,
.btn-remove-modal {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: block;
  margin-bottom: 0.5rem;
}

.btn-view {
  background: var(--color-gold-500);
  border: none;
  color: #000;
}

.btn-view:hover {
  background: var(--color-gold-600);
  transform: translateY(-2px);
}

.btn-remove-modal {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
  margin-bottom: 0;
}

.btn-remove-modal:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
}

@media (max-width: 768px) {
  .modal-container {
    max-width: 100%;
    max-height: 100vh;
    border-radius: 0;
  }
  
  .property-col {
    width: 250px;
    min-width: 250px;
  }
  
  .modal-overlay {
    padding: 1rem;
    padding-bottom: 140px;
  }
}
</style>