import type { Property, HomeHarvestListing } from '@/types/property';
import { convertApiToProperty } from '@/utils/propertyHelpers';

class DataService {
  private cache: Map<string, Property[]> = new Map();
  private baseUrl = '/data'; // Will change to API URL later

  /**
   * Load properties for a specific zip code
   */
  async loadPropertiesByZip(zipCode: string): Promise<Property[]> {
    // Check cache first
    if (this.cache.has(zipCode)) {
      return this.cache.get(zipCode)!;
    }

    try {
      // Load from public/data directory (will switch to API later)
      const response = await fetch(`${this.baseUrl}/az/${zipCode}.json`);
      
      if (!response.ok) {
        throw new Error(`Failed to load data for zip ${zipCode}`);
      }

      const listings: HomeHarvestListing[] = await response.json();
      const properties = listings.map(listing => convertApiToProperty(listing));
      
      // Cache the results
      this.cache.set(zipCode, properties);
      
      return properties;
    } catch (error) {
      console.error(`Error loading properties for zip ${zipCode}:`, error);
      return [];
    }
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
   * Get all available Arizona properties (from our sample data)
   */
  async loadAllArizonaProperties(): Promise<Property[]> {
    // For now, load our sample zip codes
    const sampleZips = ['85001', '85003', '85004', '85254', '85260'];
    return this.loadPropertiesByZips(sampleZips);
  }

  /**
   * Search properties by city (future enhancement)
   */
  async searchByCity(city: string, state: string = 'AZ'): Promise<Property[]> {
    // TODO: Implement when backend is ready
    // For now, load all available properties and filter
    const allProperties = await this.loadAllArizonaProperties();
    return allProperties.filter(p => 
      p.city?.toLowerCase().includes(city.toLowerCase())
    );
  }

  /**
   * Clear the cache (useful for development)
   */
  clearCache(): void {
    this.cache.clear();
  }

  /**
   * Future: Switch to API mode
   * Uncomment this when backend is ready
   */
  // async loadPropertiesByZip(zipCode: string): Promise<Property[]> {
  //   const response = await fetch(`${this.baseUrl}/api/properties/zip/${zipCode}`);
  //   const data = await response.json();
  //   return data.properties;
  // }
}

// Export singleton instance
export const dataService = new DataService();