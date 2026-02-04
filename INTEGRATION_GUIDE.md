# Frontend-Backend Integration Guide

## ✅ What's Been Completed

### 1. Backend API Integration
The [dataService.ts](frontend/src/services/realEstate/dataService.ts) is **fully configured** to connect to the backend API at `http://localhost:8000`.

### 2. Properties Store Updates
The [properties.ts](frontend/src/stores/properties.ts) store has been **upgraded** with:
- ✅ Server-side filtering (filters sent to API, not applied client-side)
- ✅ Pagination state management (currentPage, pageSize, totalCount)
- ✅ Pagination methods (nextPage, previousPage, goToPage, setPageSize)
- ✅ Auto-fetch on filter changes
- ✅ Direct API property fetching

### 3. New Pagination Component
Created [Pagination.vue](frontend/src/components/property/Pagination.vue) - A reusable pagination component with:
- Page navigation buttons
- Page number display with ellipsis
- Results count display
- Page size selector
- Fully styled and responsive

---

## 🔧 How to Integrate Pagination in Views

### Example: Updating Search.vue

#### Step 1: Import the Pagination Component

```typescript
import Pagination from '@/components/property/Pagination.vue'
import { useRoute } from 'vue-router' // Add this if missing
```

#### Step 2: Update the Result Count Display

**Before:**
```vue
<p class="result-count">{{ propertiesStore.filteredProperties.length }} properties found</p>
```

**After:**
```vue
<p class="result-count">{{ propertiesStore.totalCount }} properties found</p>
```

#### Step 3: Add Pagination Component Before Closing `</main>`

Add this before the `</main>` tag (around line 176 in Search.vue):

```vue
<!-- Pagination -->
<Pagination
  v-if="!propertiesStore.loading && propertiesStore.filteredProperties.length > 0"
  :current-page="propertiesStore.currentPage"
  :total-pages="propertiesStore.totalPages"
  :total-count="propertiesStore.totalCount"
  :page-size="propertiesStore.pageSize"
  :has-next-page="propertiesStore.hasNextPage"
  :has-previous-page="propertiesStore.hasPreviousPage"
  @next="propertiesStore.nextPage()"
  @previous="propertiesStore.previousPage()"
  @goto="propertiesStore.goToPage($event)"
  @change-page-size="propertiesStore.setPageSize($event)"
/>
```

#### Step 4: Update the setFilters Calls

The store's `setFilters` and `clearFilters` methods now automatically fetch data, so no changes needed in the component logic! But note that they're now async if you want to await them:

```typescript
// The existing code will work as-is:
const updateFilters = () => {
  propertiesStore.setFilters(localFilters.value);
};

// Or make it async if you want to handle loading:
const updateFilters = async () => {
  await propertiesStore.setFilters(localFilters.value);
};
```

---

## 🚀 Testing the Integration

### 1. Start the Backend

```bash
cd /Users/shyamway/Desktop/Projects/homefinder/backend
uv run python run.py
```

Should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Visit http://localhost:8000/docs to verify the API is working.

### 2. Start the Frontend

```bash
cd /Users/shyamway/Desktop/Projects/homefinder/frontend
npm run dev
```

Should see:
```
VITE ready in XXX ms
Local: http://localhost:5173/
```

### 3. Test the Features

1. **Search Page**: Navigate to the search page
2. **Verify Data**: Should see properties loading from the API (check browser console for "Loaded page X" messages)
3. **Test Filters**: Apply filters and verify they trigger new API calls
4. **Test Pagination**: Click through pages, verify data updates
5. **Test Page Size**: Change items per page, verify it works

### 4. Browser Console Checks

Open browser DevTools and check:
- **Network tab**: Should see requests to `http://localhost:8000/api/properties/`
- **Console logs**: Should see "Fetching from API:" and "Loaded X properties" messages
- **No errors**: Check for any CORS or connection errors

---

## 📊 New Store API Reference

### State

```typescript
propertiesStore.properties         // Current page of properties
propertiesStore.totalCount          // Total count from API
propertiesStore.currentPage         // Current page number (1-indexed)
propertiesStore.pageSize            // Items per page (default: 20)
propertiesStore.loading             // Loading state
propertiesStore.error               // Error message if any
```

### Computed

```typescript
propertiesStore.totalPages          // Total number of pages
propertiesStore.hasNextPage         // Can navigate forward
propertiesStore.hasPreviousPage     // Can navigate backward
propertiesStore.filteredProperties  // Current page properties (for compatibility)
```

### Methods

```typescript
// Fetch with current filters and page
await propertiesStore.fetchProperties(resetPage?: boolean)

// Pagination
await propertiesStore.nextPage()
await propertiesStore.previousPage()
await propertiesStore.goToPage(page: number)
await propertiesStore.setPageSize(size: number)

// Filters (now auto-fetch)
await propertiesStore.setFilters(filters: PropertyFilters, autoFetch?: boolean)
await propertiesStore.clearFilters(autoFetch?: boolean)

// Single property (uses backend API directly)
await propertiesStore.fetchPropertyById(id: string)
```

---

## 🎯 Backend API Quick Reference

### Endpoints

#### GET /api/properties/
List properties with filters and pagination.

**Query Parameters:**
- `city` (string) - Filter by city (partial match)
- `state` (string) - Filter by state code (exact match)
- `zip_code` (string) - Filter by zip code
- `min_price` (int) - Minimum price
- `max_price` (int) - Maximum price
- `beds` (int) - Minimum bedrooms
- `baths` (float) - Minimum bathrooms
- `property_type` (string) - SINGLE_FAMILY, CONDO, TOWNHOUSE, LAND, MOBILE
- `status` (string) - FOR_SALE, PENDING, SOLD, OFF_MARKET
- `limit` (int) - Items per page (default: 20, max: 100)
- `offset` (int) - Items to skip (default: 0)

**Response:**
```json
{
  "total": 247941,
  "properties": [...],
  "limit": 20,
  "offset": 0
}
```

#### GET /api/properties/{id}
Get a single property by ID.

#### GET /api/properties/stats/overview
Get platform statistics.

**Response:**
```json
{
  "total_properties": 247941,
  "avg_price": 450000
}
```

---

## 🔍 Troubleshooting

### Backend Not Responding

**Check if backend is running:**
```bash
curl http://localhost:8000/api/properties/stats/overview
```

**Expected response:**
```json
{"total_properties": 247941, "avg_price": ...}
```

**If not running:**
```bash
cd backend
uv run python run.py
```

### CORS Errors

The backend is configured for both ports 5173 and 5174. If you get CORS errors, check:
1. Backend `.env` file has correct `CORS_ORIGINS`
2. Frontend is running on port 5173 or 5174

### No Data Showing

1. Check browser console for errors
2. Check Network tab for failed API calls
3. Verify backend has data:
   ```bash
   cd backend
   uv run python check_stats.py
   ```

### Filters Not Working

1. Check browser console for API request URLs
2. Verify filter values are being passed correctly
3. Check that property type/status mappings are correct

---

## 📝 Migration Checklist

- [x] Backend API running and accessible
- [x] dataService.ts connected to backend
- [x] Properties store updated with pagination
- [x] Pagination component created
- [ ] Search.vue updated with pagination
- [ ] Home.vue updated (if needed)
- [ ] Dashboard.vue updated (if needed)
- [ ] Test all filters work correctly
- [ ] Test pagination works correctly
- [ ] Test on mobile devices
- [ ] Remove old static JSON files (optional)

---

## 🎉 What You Get

After integration, your app will:
- ✅ Access all **247,941 properties** across all states
- ✅ Fast searches with **server-side filtering**
- ✅ Efficient **pagination** (only load 20-100 properties at a time)
- ✅ Real-time updates from **PostgreSQL database**
- ✅ Better performance (no loading 247K properties into memory)
- ✅ Professional pagination UI

---

**Last Updated:** February 3, 2026
