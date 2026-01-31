<template>
  <div class="map-container">
    <div ref="mapElement" class="map" />
    
    <!-- Map Controls -->
    <div v-if="isFiltered && onResetFilter" class="map-controls">
      <button class="btn btn-secondary" @click="onResetFilter">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
          <path d="M3 3v5h5"/>
        </svg>
        Clear Filters
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
import L from 'leaflet';
import type { Property } from '@/types/property';
import { formatPrice } from '@/utils/propertyHelpers';

interface Props {
  properties: Property[];
  isFiltered?: boolean;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  select: [property: Property];
  resetFilter?: [];
}>();

const mapElement = ref<HTMLDivElement | null>(null);
let map: L.Map | null = null;
let markers: L.CircleMarker[] = [];

const initMap = () => {
  if (!mapElement.value || map) return;

  // Initialize map
  map = L.map(mapElement.value, {
    zoomControl: true,
    attributionControl: false
  }).setView([33.4484, -112.0740], 10); // Phoenix default

  // Add tile layer (dark theme)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(map);
};

const clearMarkers = () => {
  markers.forEach(marker => marker.remove());
  markers = [];
};

const addMarkers = () => {
  if (!map) return;

  clearMarkers();

  const bounds = L.latLngBounds([]);
  
  props.properties.forEach(property => {
    if (!property.coordinates.lat || !property.coordinates.lng) return;

    // Create custom gold circle marker
    const marker = L.circleMarker(
      [property.coordinates.lat, property.coordinates.lng],
      {
        color: '#D4AF37',
        fillColor: '#C5A028',
        fillOpacity: 1,
        radius: 8,
        weight: 2
      }
    ).addTo(map!);

    // Create popup content
    const popupContent = createPopupContent(property);
    
    const popup = L.popup({
      closeButton: false,
      maxWidth: 280,
      minWidth: 260,
      className: 'custom-map-popup',
      offset: [0, -4]
    }).setContent(popupContent);

    marker.bindPopup(popup);

    // Event handlers
    marker.on('mouseover', () => {
      marker.openPopup();
    });

    marker.on('mouseout', () => {
      marker.closePopup();
    });

    marker.on('click', () => {
      emit('select', property);
    });

    // Also close popup when mouse leaves the popup itself
    popup.on('remove', () => {
      // Popup closed
    });

    markers.push(marker);
    bounds.extend([property.coordinates.lat, property.coordinates.lng]);
  });

  // Fit map to show all markers
  if (props.properties.length > 0 && bounds.isValid()) {
    map!.fitBounds(bounds, { padding: [50, 50], maxZoom: 13 });
  }
};

const createPopupContent = (property: Property): HTMLElement => {
  const container = document.createElement('div');
  container.className = 'popup-container';
  
  container.innerHTML = `
    <div class="popup-image">
      <img src="${property.image}" alt="${property.title}" />
      <div class="popup-overlay"></div>
      <div class="popup-badge">
        <span>${property.type}</span>
      </div>
    </div>
    <div class="popup-content">
      <h3 class="popup-title">${property.title}</h3>
      <p class="popup-location">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/>
          <circle cx="12" cy="10" r="3"/>
        </svg>
        ${property.location}
      </p>
      <div class="popup-footer">
        <span class="popup-price">${formatPrice(property.price)}</span>
        <span class="popup-cta">
          View
          <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14"/>
            <path d="m12 5 7 7-7 7"/>
          </svg>
        </span>
      </div>
    </div>
  `;

  // Add click handler
  container.addEventListener('click', (e) => {
    e.stopPropagation();
    emit('select', property);
  });

  return container;
};

const onResetFilter = () => {
  emit('resetFilter');
};

// Lifecycle
onMounted(() => {
  initMap();
  addMarkers();
});

onBeforeUnmount(() => {
  if (map) {
    map.remove();
    map = null;
  }
});

// Watch for property changes
watch(() => props.properties, () => {
  addMarkers();
}, { deep: true });
</script>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 600px;
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-xl);
}

.map {
  width: 100%;
  height: 100%;
  background: var(--color-surface);
}

.map-controls {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 1000;
}

/* Custom popup styles - Need to be global */
:deep(.leaflet-popup-content-wrapper) {
  padding: 0;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
}

:deep(.leaflet-popup-content) {
  margin: 0;
  width: 260px !important;
}

:deep(.leaflet-popup-tip) {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
}

:deep(.popup-container) {
  cursor: pointer;
  background: var(--color-surface);
  transition: transform 0.2s ease;
}

:deep(.popup-container:hover) {
  transform: translateY(-2px);
}

:deep(.popup-image) {
  position: relative;
  height: 140px;
  overflow: hidden;
}

:deep(.popup-image img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

:deep(.popup-container:hover .popup-image img) {
  transform: scale(1.1);
}

:deep(.popup-overlay) {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.6), transparent);
}

:deep(.popup-badge) {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  z-index: 10;
}

:deep(.popup-badge span) {
  background: rgba(255, 255, 255, 0.9);
  color: var(--color-gold-600);
  border: 1px solid rgba(212, 175, 55, 0.2);
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  backdrop-filter: blur(8px);
}

:deep(.popup-content) {
  padding: 1rem;
}

:deep(.popup-title) {
  font-family: var(--font-family-serif);
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 0.25rem;
  line-height: 1.3;
}

:deep(.popup-location) {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 11px;
  color: var(--color-text-secondary);
  margin-bottom: 0.75rem;
}

:deep(.popup-location svg) {
  color: var(--color-gold-500);
  flex-shrink: 0;
}

:deep(.popup-footer) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid var(--color-border);
}

:deep(.popup-price) {
  font-family: var(--font-family-display);
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: var(--color-text);
}

:deep(.popup-cta) {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-gold-500);
  transition: transform 0.2s ease;
}

:deep(.popup-container:hover .popup-cta) {
  transform: translateX(4px);
}

@media (prefers-color-scheme: dark) {
  :deep(.popup-badge span) {
    background: rgba(0, 0, 0, 0.8);
    color: var(--color-gold-400);
  }
}
</style>