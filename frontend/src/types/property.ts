export interface Property {
  id: string;
  title: string;
  price: number;
  location: string;
  sqft: number;
  beds: number;
  baths: number;
  image: string;
  description: string;
  features: string[];
  type: 'House' | 'Condo' | 'Townhouse' | 'Land' | 'Mobile' | 'Other';
  yearBuilt: number;
  history: { date: string; price: number }[];
  coordinates: { lat: number; lng: number };
  floorPlan?: string;
  
  // Additional fields from your React version
  propertyUrl?: string;
  status?: 'Active' | 'Pending' | 'Sold' | 'Off Market';
  street?: string;
  city?: string;
  state?: string;
  zipCode?: string;
  lotSqft?: number;
  hoaFee?: number;
  agentName?: string;
  officeName?: string;
  altPhotos?: string[];
}

// API data structure (for future backend integration)
export interface HomeHarvestListing {
  property_id: string;
  property_url: string;
  listing_id: string;
  status: string;
  mls_status: string;
  text: string;
  style: string;
  formatted_address: string;
  full_street_line: string;
  street: string;
  unit: string | null;
  city: string;
  state: string;
  zip_code: string;
  beds: number | null;
  full_baths: number | null;
  half_baths: number | null;
  sqft: number | null;
  year_built: number | null;
  days_on_mls: number;
  list_price: number | null;
  list_price_min: number | null;
  list_price_max: number | null;
  list_date: string;
  sold_price: number | null;
  last_sold_date: string | null;
  last_sold_price: number | null;
  assessed_value: number | null;
  estimated_value: number | null;
  lot_sqft: number | null;
  latitude: number;
  longitude: number;
  county: string;
  stories: number | null;
  hoa_fee: number | null;
  parking_garage: number | null;
  agent_name: string | null;
  office_name: string | null;
  primary_photo: string | null;
  alt_photos: string | null;
}

export interface PropertyFilters {
  minPrice?: number;
  maxPrice?: number;
  minBedrooms?: number;
  minBathrooms?: number;
  propertyType?: Property['type'];
  city?: string;
  state?: string;
  status?: Property['status'];
}