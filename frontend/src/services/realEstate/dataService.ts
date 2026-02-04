import type { Property } from '@/types/property';

// Backend API response interfaces
interface PropertyResponse {
  id: string;
  title: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  price: number;
  beds: number | null;
  baths: number | null;
  sqft: number | null;
  lot_sqft: number | null;
  year_built: number | null;
  property_type: string;
  status: string;
  latitude: number | null;
  longitude: number | null;
  description: string | null;
  features: string[];
  hoa_fee: number | null;
  image: string | null;
  alt_photos: string[];
  agent_name: string | null;
  agent_phone: string | null;
  office_name: string | null;
  property_url: string | null;
  mls_number: string | null;
  price_history: any[];
  is_featured: boolean;
  created_at: string;
  updated_at: string | null;
}

interface PropertyListResponse {
  total: number;
  properties: PropertyResponse[];
  limit: number;
  offset: number;
}

interface SearchParams {
  city?: string;
  state?: string;
  zip_code?: string;
  min_price?: number;
  max_price?: number;
  beds?: number;
  baths?: number;
  property_type?: string;
  status?: string;
  limit?: number;
  offset?: number;
}

class DataService {
  private baseUrl = 'http://localhost:8000'; // Backend API URL
  private cache: Map<string, Property[]> = new Map();

  /**
   * Convert backend PropertyResponse to frontend Property type
   */
  private convertToProperty(apiProperty: PropertyResponse): Property {
    // Map backend property_type to frontend type enum
    const typeMap: Record<string, Property['type']> = {
      'SINGLE_FAMILY': 'House',
      'CONDO': 'Condo',
      'TOWNHOUSE': 'Townhouse',
      'LAND': 'Land',
      'MOBILE': 'Mobile',
      'MULTI_FAMILY': 'House'
    };

    // Map backend status to frontend status
    const statusMap: Record<string, Property['status']> = {
      'FOR_SALE': 'Active',
      'PENDING': 'Pending',
      'SOLD': 'Sold',
      'OFF_MARKET': 'Off Market'
    };

    return {
      id: apiProperty.id,
      title: apiProperty.title,
      price: apiProperty.price,
      location: `${apiProperty.city}, ${apiProperty.state} ${apiProperty.zip_code}`,
      sqft: apiProperty.sqft || 0,
      beds: apiProperty.beds || 0,
      baths: apiProperty.baths || 0,
      image: apiProperty.image || '/placeholder.jpg',
      description: apiProperty.description || 'No description available',
      features: apiProperty.features || [],
      type: typeMap[apiProperty.property_type] || 'Other',
      yearBuilt: apiProperty.year_built || 0,
      history: apiProperty.price_history || [],
      coordinates: {
        lat: apiProperty.latitude || 0,
        lng: apiProperty.longitude || 0
      },
      // Additional fields
      propertyUrl: apiProperty.property_url || undefined,
      status: statusMap[apiProperty.status] || 'Active',
      street: apiProperty.address,
      city: apiProperty.city,
      state: apiProperty.state,
      zipCode: apiProperty.zip_code,
      lotSqft: apiProperty.lot_sqft || undefined,
      hoaFee: apiProperty.hoa_fee || undefined,
      agentName: apiProperty.agent_name || undefined,
      officeName: apiProperty.office_name || undefined,
      altPhotos: apiProperty.alt_photos || []
    };
  }

  /**
   * Search properties with filters
   */
  async searchProperties(params: SearchParams = {}): Promise<{ properties: Property[], total: number }> {
    try {
      const queryParams = new URLSearchParams();
      
      if (params.city) queryParams.append('city', params.city);
      if (params.state) queryParams.append('state', params.state);
      if (params.zip_code) queryParams.append('zip_code', params.zip_code);
      if (params.min_price !== undefined) queryParams.append('min_price', params.min_price.toString());
      if (params.max_price !== undefined) queryParams.append('max_price', params.max_price.toString());
      if (params.beds !== undefined) queryParams.append('beds', params.beds.toString());
      if (params.baths !== undefined) queryParams.append('baths', params.baths.toString());
      if (params.property_type) queryParams.append('property_type', params.property_type);
      if (params.status) queryParams.append('status', params.status);
      
      // Pagination
      const limit = params.limit || 20;
      const offset = params.offset || 0;
      queryParams.append('limit', limit.toString());
      queryParams.append('offset', offset.toString());

      const url = `${this.baseUrl}/api/properties/?${queryParams.toString()}`;
      console.log('Fetching from API:', url);

      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data: PropertyListResponse = await response.json();
      const properties = data.properties.map(p => this.convertToProperty(p));
      
      console.log(`Loaded ${properties.length} properties out of ${data.total} total`);
      
      return {
        properties,
        total: data.total
      };
    } catch (error) {
      console.error('Error searching properties:', error);
      throw error;
    }
  }

  /**
   * Load properties for a specific zip code
   */
  async loadPropertiesByZip(zipCode: string): Promise<Property[]> {
    const result = await this.searchProperties({ zip_code: zipCode, limit: 100 });
    return result.properties;
  }

  /**
   * Load properties from multiple zip codes
   */
  async loadPropertiesByZips(zipCodes: string[]): Promise<Property[]> {
    const allProperties: Property[] = [];
    
    for (const zip of zipCodes) {
      const properties = await this.loadPropertiesByZip(zip);
      allProperties.push(...properties);
    }
    
    return allProperties;
  }

  /**
   * Get a single property by ID
   */
  async getPropertyById(id: string): Promise<Property> {
    try {
      const response = await fetch(`${this.baseUrl}/api/properties/${id}`);
      
      if (!response.ok) {
        throw new Error(`Property not found: ${id}`);
      }

      const data: PropertyResponse = await response.json();
      return this.convertToProperty(data);
    } catch (error) {
      console.error(`Error loading property ${id}:`, error);
      throw error;
    }
  }

  /**
   * Get platform statistics
   */
  async getStats(): Promise<{ total_properties: number; avg_price: number }> {
    try {
      const response = await fetch(`${this.baseUrl}/api/properties/stats/overview`);
      
      if (!response.ok) {
        throw new Error('Failed to load stats');
      }

      return await response.json();
    } catch (error) {
      console.error('Error loading stats:', error);
      throw error;
    }
  }

  /**
   * Search properties by city
   */
  async searchByCity(city: string, state?: string): Promise<Property[]> {
    const result = await this.searchProperties({ city, state, limit: 100 });
    return result.properties;
  }

  /**
   * Load all properties (with pagination)
   */
  async loadAllProperties(limit: number = 20, offset: number = 0): Promise<{ properties: Property[], total: number }> {
    return this.searchProperties({ limit, offset });
  }

  /**
   * Load all available properties (backward compatibility)
   */
  async loadAllArizonaProperties(): Promise<Property[]> {
    const result = await this.searchProperties({ state: 'AZ', limit: 100 });
    return result.properties;
  }

  /**
   * Clear the cache (useful for development)
   */
  clearCache(): void {
    this.cache.clear();
  }
}

// Export singleton instance
export const dataService = new DataService();