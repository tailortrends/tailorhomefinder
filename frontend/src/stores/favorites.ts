import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Property } from '@/types/property'

export const useFavoritesStore = defineStore('favorites', () => {
  // State
  const favorites = ref<Property[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const favoriteIds = computed(() => 
    favorites.value.map(p => p.property_id)
  )

  const favoritesCount = computed(() => favorites.value.length)

  const hasFavorites = computed(() => favorites.value.length > 0)

  // Check if property is favorited
  function isFavorited(propertyId: string): boolean {
    return favoriteIds.value.includes(propertyId)
  }

  // Actions
  async function loadFavorites() {
    loading.value = true
    error.value = null

    try {
      // Load from localStorage for now
      const stored = localStorage.getItem('user_favorites')
      if (stored) {
        favorites.value = JSON.parse(stored)
      }

      // In production, this would fetch from backend:
      // const response = await fetch('/api/favorites')
      // favorites.value = await response.json()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load favorites'
      console.error('Error loading favorites:', err)
    } finally {
      loading.value = false
    }
  }

  async function addFavorite(property: Property) {
    // Check if already favorited
    if (isFavorited(property.property_id)) {
      return
    }

    loading.value = true
    error.value = null

    try {
      // Add to local state
      favorites.value.push(property)

      // Save to localStorage
      localStorage.setItem('user_favorites', JSON.stringify(favorites.value))

      // In production, this would call backend API:
      // await fetch('/api/favorites', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ property_id: property.property_id })
      // })
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to add favorite'
      console.error('Error adding favorite:', err)
      
      // Rollback on error
      favorites.value = favorites.value.filter(p => p.property_id !== property.property_id)
    } finally {
      loading.value = false
    }
  }

  async function removeFavorite(propertyId: string) {
    const index = favorites.value.findIndex(p => p.property_id === propertyId)
    if (index === -1) return

    // Store the removed property for potential rollback
    const removed = favorites.value[index]

    loading.value = true
    error.value = null

    try {
      // Remove from local state
      favorites.value.splice(index, 1)

      // Save to localStorage
      localStorage.setItem('user_favorites', JSON.stringify(favorites.value))

      // In production, this would call backend API:
      // await fetch(`/api/favorites/${propertyId}`, {
      //   method: 'DELETE'
      // })
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to remove favorite'
      console.error('Error removing favorite:', err)
      
      // Rollback on error
      favorites.value.splice(index, 0, removed)
    } finally {
      loading.value = false
    }
  }

  async function toggleFavorite(property: Property) {
    if (isFavorited(property.property_id)) {
      await removeFavorite(property.property_id)
    } else {
      await addFavorite(property)
    }
  }

  function clearFavorites() {
    favorites.value = []
    localStorage.removeItem('user_favorites')
  }

  // Sort favorites
  function sortByNewest() {
    favorites.value.sort((a, b) => {
      const dateA = new Date(a.list_date || a.created_at || 0).getTime()
      const dateB = new Date(b.list_date || b.created_at || 0).getTime()
      return dateB - dateA
    })
  }

  function sortByPrice(ascending = true) {
    favorites.value.sort((a, b) => {
      return ascending 
        ? a.list_price - b.list_price 
        : b.list_price - a.list_price
    })
  }

  function sortByBeds(ascending = false) {
    favorites.value.sort((a, b) => {
      return ascending 
        ? a.beds - b.beds 
        : b.beds - a.beds
    })
  }

  return {
    // State
    favorites,
    loading,
    error,
    
    // Computed
    favoriteIds,
    favoritesCount,
    hasFavorites,
    
    // Methods
    isFavorited,
    loadFavorites,
    addFavorite,
    removeFavorite,
    toggleFavorite,
    clearFavorites,
    sortByNewest,
    sortByPrice,
    sortByBeds
  }
})
