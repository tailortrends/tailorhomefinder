import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Property, PropertyFilters, PropertySearchResult } from '@/types/property'

export const usePropertiesStore = defineStore('properties', () => {
  // State
  const properties = ref<Property[]>([])
  const currentProperty = ref<Property | null>(null)
  const filters = ref<PropertyFilters>({
    location: '',
    minPrice: undefined,
    maxPrice: undefined,
    minBeds: undefined,
    minBaths: undefined,
    propertyType: undefined,
    minSqft: undefined,
    maxSqft: undefined
  })
  
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  // Pagination
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalProperties = ref(0)
  const pageSize = ref(12)
  
  // Sorting
  const sortBy = ref<'price' | 'price_desc' | 'newest' | 'sqft' | 'beds'>('newest')

  // Computed
  const hasFilters = computed(() => {
    return !!(
      filters.value.minPrice ||
      filters.value.maxPrice ||
      filters.value.minBeds ||
      filters.value.minBaths ||
      filters.value.propertyType ||
      filters.value.minSqft ||
      filters.value.maxSqft
    )
  })

  const filteredProperties = computed(() => {
    let filtered = [...properties.value]

    // Apply filters
    if (filters.value.minPrice) {
      filtered = filtered.filter(p => p.list_price >= filters.value.minPrice!)
    }
    if (filters.value.maxPrice) {
      filtered = filtered.filter(p => p.list_price <= filters.value.maxPrice!)
    }
    if (filters.value.minBeds) {
      filtered = filtered.filter(p => p.beds >= filters.value.minBeds!)
    }
    if (filters.value.minBaths) {
      filtered = filtered.filter(p => p.full_baths >= filters.value.minBaths!)
    }
    if (filters.value.propertyType) {
      filtered = filtered.filter(p => p.property_type === filters.value.propertyType)
    }
    if (filters.value.minSqft && filters.value.minSqft > 0) {
      filtered = filtered.filter(p => p.sqft && p.sqft >= filters.value.minSqft!)
    }
    if (filters.value.maxSqft && filters.value.maxSqft > 0) {
      filtered = filtered.filter(p => p.sqft && p.sqft <= filters.value.maxSqft!)
    }

    // Apply sorting
    switch (sortBy.value) {
      case 'price':
        filtered.sort((a, b) => a.list_price - b.list_price)
        break
      case 'price_desc':
        filtered.sort((a, b) => b.list_price - a.list_price)
        break
      case 'sqft':
        filtered.sort((a, b) => (b.sqft || 0) - (a.sqft || 0))
        break
      case 'beds':
        filtered.sort((a, b) => b.beds - a.beds)
        break
      case 'newest':
      default:
        filtered.sort((a, b) => {
          const dateA = new Date(a.list_date || a.created_at || 0).getTime()
          const dateB = new Date(b.list_date || b.created_at || 0).getTime()
          return dateB - dateA
        })
    }

    return filtered
  })

  const paginatedProperties = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return filteredProperties.value.slice(start, end)
  })

  // Actions
  async function fetchProperties(zipCode?: string) {
    loading.value = true
    error.value = null

    try {
      // If zipCode is provided, fetch from local JSON files
      if (zipCode) {
        const response = await fetch(`/data/az/${zipCode}.json`)
        if (!response.ok) throw new Error('Failed to fetch properties')
        const data = await response.json()
        properties.value = data
      } else {
        // Fetch all properties from available files
        const zipCodes = ['85001', '85003', '85004', '85254', '85260']
        const allProperties: Property[] = []
        
        for (const zip of zipCodes) {
          try {
            const response = await fetch(`/data/az/${zip}.json`)
            if (response.ok) {
              const data = await response.json()
              allProperties.push(...data)
            }
          } catch (err) {
            console.warn(`Failed to fetch data for ZIP ${zip}`)
          }
        }
        
        properties.value = allProperties
      }

      // Update pagination
      totalProperties.value = filteredProperties.value.length
      totalPages.value = Math.ceil(totalProperties.value / pageSize.value)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An error occurred'
      console.error('Error fetching properties:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchPropertyById(id: string) {
    loading.value = true
    error.value = null

    try {
      // Search in current properties first
      const found = properties.value.find(p => p.property_id === id)
      if (found) {
        currentProperty.value = found
        return found
      }

      // If not found, try to fetch from API or files
      // This would be replaced with actual API call
      await fetchProperties()
      const property = properties.value.find(p => p.property_id === id)
      currentProperty.value = property || null
      return property
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An error occurred'
      console.error('Error fetching property:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  function updateFilters(newFilters: Partial<PropertyFilters>) {
    filters.value = { ...filters.value, ...newFilters }
    currentPage.value = 1 // Reset to first page when filters change
    
    // Update pagination with filtered results
    totalProperties.value = filteredProperties.value.length
    totalPages.value = Math.ceil(totalProperties.value / pageSize.value)
  }

  function resetFilters() {
    filters.value = {
      location: filters.value.location, // Keep location
      minPrice: undefined,
      maxPrice: undefined,
      minBeds: undefined,
      minBaths: undefined,
      propertyType: undefined,
      minSqft: undefined,
      maxSqft: undefined
    }
    currentPage.value = 1
    
    // Update pagination
    totalProperties.value = filteredProperties.value.length
    totalPages.value = Math.ceil(totalProperties.value / pageSize.value)
  }

  function setSortBy(sort: typeof sortBy.value) {
    sortBy.value = sort
  }

  function setPage(page: number) {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }

  function nextPage() {
    if (currentPage.value < totalPages.value) {
      currentPage.value++
    }
  }

  function prevPage() {
    if (currentPage.value > 1) {
      currentPage.value--
    }
  }

  return {
    // State
    properties,
    currentProperty,
    filters,
    loading,
    error,
    currentPage,
    totalPages,
    totalProperties,
    pageSize,
    sortBy,
    
    // Computed
    hasFilters,
    filteredProperties,
    paginatedProperties,
    
    // Actions
    fetchProperties,
    fetchPropertyById,
    updateFilters,
    resetFilters,
    setSortBy,
    setPage,
    nextPage,
    prevPage
  }
})
