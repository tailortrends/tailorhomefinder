import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Property, PropertyFilters } from '@/types/property';

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
      result = result.filter(p => p.bedrooms >= filters.value.minBedrooms!);
    }
    if (filters.value.minBathrooms) {
      result = result.filter(p => p.bathrooms >= filters.value.minBathrooms!);
    }
    if (filters.value.propertyType) {
      result = result.filter(p => p.propertyType === filters.value.propertyType);
    }
    if (filters.value.city) {
      result = result.filter(p => 
        p.city.toLowerCase().includes(filters.value.city!.toLowerCase())
      );
    }
    if (filters.value.state) {
      result = result.filter(p => p.state === filters.value.state);
    }

    return result;
  });

  // Actions
  const fetchProperties = async () => {
    loading.value = true;
    error.value = null;
    try {
      // TODO: Replace with actual Firebase/API call
      // For now, this is a placeholder
      properties.value = [];
    } catch (err: any) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };

  const fetchPropertyById = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      // TODO: Replace with actual Firebase/API call
      selectedProperty.value = properties.value.find(p => p.id === id) || null;
    } catch (err: any) {
      error.value = err.message;
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
    fetchPropertyById,
    setFilters,
    clearFilters
  };
});