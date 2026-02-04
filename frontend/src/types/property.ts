// Property Type Definitions

export interface Property {
  property_id: string
  mls_id?: string
  status: 'for_sale' | 'pending' | 'sold' | 'off_market'
  
  // Basic Info
  list_price: number
  price_per_sqft?: number
  
  // Location
  full_street_line: string
  street: string
  city: string
  state: string
  zip_code: string
  county?: string
  latitude?: number
  longitude?: number
  
  // Property Details
  beds: number
  full_baths: number
  half_baths?: number
  sqft?: number
  lot_sqft?: number
  year_built?: number
  property_type: string
  style?: string
  
  // Media
  primary_photo?: string
  photos?: string[]
  
  // Additional Info
  description?: string
  hoa_fee?: number
  parking_garage?: number
  days_on_mls?: number
  list_date?: string
  last_sold_date?: string
  last_sold_price?: number
  
  // Agent/Listing Info
  listing_agent?: string
  listing_office?: string
  mls?: string
  
  // Computed/Helper
  created_at?: string
  updated_at?: string
}

export interface PropertyFilters {
  location?: string
  minPrice?: number
  maxPrice?: number
  minBeds?: number
  maxBeds?: number
  minBaths?: number
  maxBaths?: number
  minSqft?: number
  maxSqft?: number
  propertyType?: string
  status?: string
  zipCode?: string
  city?: string
  state?: string
}

export interface PropertySearchParams extends PropertyFilters {
  page?: number
  limit?: number
  sortBy?: 'price' | 'price_desc' | 'newest' | 'sqft' | 'beds'
}

export interface PropertySearchResult {
  properties: Property[]
  total: number
  page: number
  totalPages: number
  hasMore: boolean
}

// Helper Types
export interface PriceRange {
  label: string
  min?: number
  max?: number
}

export interface FilterOption<T = any> {
  label: string
  value: T
}

// Constants
export const PRICE_RANGES: PriceRange[] = [
  { label: 'Any Price', min: undefined, max: undefined },
  { label: '$0 - $500k', min: 0, max: 500000 },
  { label: '$500k - $1M', min: 500000, max: 1000000 },
  { label: '$1M - $2M', min: 1000000, max: 2000000 },
  { label: '$2M - $5M', min: 2000000, max: 5000000 },
  { label: '$5M+', min: 5000000, max: undefined }
]

export const PROPERTY_TYPES: FilterOption<string>[] = [
  { label: 'All Types', value: '' },
  { label: 'Single Family', value: 'single_family_residential' },
  { label: 'Condo', value: 'condo' },
  { label: 'Townhouse', value: 'townhouse' },
  { label: 'Multi-Family', value: 'multi_family' },
  { label: 'Land', value: 'land' }
]

export const BEDROOM_OPTIONS: FilterOption<number | undefined>[] = [
  { label: 'Any', value: undefined },
  { label: '1+', value: 1 },
  { label: '2+', value: 2 },
  { label: '3+', value: 3 },
  { label: '4+', value: 4 },
  { label: '5+', value: 5 }
]

export const BATHROOM_OPTIONS: FilterOption<number | undefined>[] = [
  { label: 'Any', value: undefined },
  { label: '1+', value: 1 },
  { label: '2+', value: 2 },
  { label: '3+', value: 3 },
  { label: '4+', value: 4 }
]

export const SORT_OPTIONS: FilterOption<string>[] = [
  { label: 'Newest', value: 'newest' },
  { label: 'Price: Low to High', value: 'price' },
  { label: 'Price: High to Low', value: 'price_desc' },
  { label: 'Square Feet', value: 'sqft' },
  { label: 'Bedrooms', value: 'beds' }
]

// Comparison feature types
export interface PropertyComparison {
  properties: Property[]
  maxProperties: number
}
