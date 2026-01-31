import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Property, PropertyFilters } from '@/types/property';
import { dataService } from '@/services/realEstate/dataService';

export const usePropertiesStore = defineStore('properties', () => {
  const properties = ref<Property[]>([]);
  const selectedProperty = ref<Property | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const filters = ref<PropertyFilters>({});

  // Computed
  const filteredProperties = computed(() => {
    let result = properties.value;

    if (filters.value.minPrice) {
      result = result.filter(p => p.price >= filters.value.minPrice!);
    }
    if (filters.value.maxPrice) {
      result = result.filter(p => p.price <= filters.value.maxPrice!);
    }
    if (filters.value.minBedrooms) {
      result = result.filter(p => p.beds >= filters.value.minBedrooms!);  // ← Changed from bedrooms to beds
    }
    if (filters.value.minBathrooms) {
      result = result.filter(p => p.baths >= filters.value.minBathrooms!);  // ← Changed from bathrooms to baths
    }
    if (filters.value.propertyType) {
      result = result.filter(p => p.type === filters.value.propertyType);  // ← Changed from propertyType to type
    }
    if (filters.value.city) {
      result = result.filter(p => 
        p.city?.toLowerCase().includes(filters.value.city!.toLowerCase())
      );
    }
    if (filters.value.state) {
      result = result.filter(p => p.state === filters.value.state);
    }
    if (filters.value.status) {
      result = result.filter(p => p.status === filters.value.status);
    }

    return result;
  });

  // Actions
  const fetchProperties = async () => {
    loading.value = true;
    error.value = null;
    try {
      // Load all available Arizona properties
      properties.value = await dataService.loadAllArizonaProperties();
    } catch (err: any) {
      error.value = err.message || 'Failed to load properties';
      console.error('Error fetching properties:', err);
    } finally {
      loading.value = false;
    }
  };

  const fetchPropertiesByZip = async (zipCode: string) => {
    loading.value = true;
    error.value = null;
    try {
      properties.value = await dataService.loadPropertiesByZip(zipCode);
    } catch (err: any) {
      error.value = err.message || 'Failed to load properties';
      console.error('Error fetching properties by zip:', err);
    } finally {
      loading.value = false;
    }
  };

  const fetchPropertiesByCity = async (city: string) => {
    loading.value = true;
    error.value = null;
    try {
      properties.value = await dataService.searchByCity(city);
    } catch (err: any) {
      error.value = err.message || 'Failed to load properties';
      console.error('Error fetching properties by city:', err);
    } finally {
      loading.value = false;
    }
  };

  const fetchPropertyById = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      // First check if property is already in store
      const existing = properties.value.find(p => p.id === id);
      if (existing) {
        selectedProperty.value = existing;
        return;
      }

      // If not, we'll need to search through available data
      // For now, load all properties and find it
      if (properties.value.length === 0) {
        await fetchProperties();
      }
      
      selectedProperty.value = properties.value.find(p => p.id === id) || null;
      
      if (!selectedProperty.value) {
        error.value = 'Property not found';
      }
    } catch (err: any) {
      error.value = err.message || 'Failed to load property';
      console.error('Error fetching property:', err);
    } finally {
      loading.value = false;
    }
  };

  const setFilters = (newFilters: PropertyFilters) => {
    filters.value = { ...filters.value, ...newFilters };
  };

  const clearFilters = () => {
    filters.value = {};
  };

  return {
    properties,
    selectedProperty,
    loading,
    error,
    filters,
    filteredProperties,
    fetchProperties,
    fetchPropertiesByZip,
    fetchPropertiesByCity,
    fetchPropertyById,
    setFilters,
    clearFilters
  };
});