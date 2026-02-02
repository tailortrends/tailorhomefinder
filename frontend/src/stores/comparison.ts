import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Property } from '@/types/property'

export const useComparisonStore = defineStore('comparison', () => {
  const comparisonList = ref<Property[]>([])
  const maxComparisons = 3

  const canAddMore = computed(() => comparisonList.value.length < maxComparisons)
  
  const isInComparison = (propertyId: string) => {
    return comparisonList.value.some(p => p.id === propertyId)
  }

  const addToComparison = (property: Property) => {
    if (comparisonList.value.length >= maxComparisons) {
      return false
    }
    if (!isInComparison(property.id)) {
      comparisonList.value.push(property)
      return true
    }
    return false
  }

  const removeFromComparison = (propertyId: string) => {
    comparisonList.value = comparisonList.value.filter(p => p.id !== propertyId)
  }

  const clearComparison = () => {
    comparisonList.value = []
  }

  const toggleComparison = (property: Property) => {
    if (isInComparison(property.id)) {
      removeFromComparison(property.id)
      return false
    } else {
      return addToComparison(property)
    }
  }

  return {
    comparisonList,
    maxComparisons,
    canAddMore,
    isInComparison,
    addToComparison,
    removeFromComparison,
    clearComparison,
    toggleComparison
  }
})