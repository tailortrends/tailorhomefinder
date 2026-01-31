cat > types/property.ts << 'EOF'
export interface Property {
  id: string;
  address: string;
  city: string;
  state: string;
  zipCode: string;
  price: number;
  bedrooms: number;
  bathrooms: number;
  squareFeet: number;
  lotSize?: number;
  yearBuilt?: number;
  propertyType: 'single-family' | 'condo' | 'townhouse' | 'multi-family' | 'land';
  status: 'for-sale' | 'pending' | 'sold' | 'off-market';
  images: string[];
  description?: string;
  features?: string[];
  listingAgent?: string;
  listingDate?: Date;
  soldDate?: Date;
  lastUpdated: Date;
}

export interface PropertyFilters {
  minPrice?: number;
  maxPrice?: number;
  minBedrooms?: number;
  minBathrooms?: number;
  propertyType?: Property['propertyType'];
  city?: string;
  state?: string;
}
EOF