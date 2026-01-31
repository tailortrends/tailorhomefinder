import type { Property, HomeHarvestListing } from '@/types/property';

// Convert API data to our Property format
export function convertApiToProperty(listing: HomeHarvestListing): Property {
  const fullBaths = listing.full_baths || 0;
  const halfBaths = listing.half_baths || 0;
  const totalBaths = fullBaths + (halfBaths * 0.5);

  // Parse alt_photos string into array
  let images: string[] = [];
  if (listing.primary_photo) {
    images.push(listing.primary_photo);
  }
  if (listing.alt_photos && typeof listing.alt_photos === 'string') {
    const altPhotosArray = listing.alt_photos.split(',').map(url => url.trim());
    images = images.concat(altPhotosArray);
  }

  // Create property title from address
  const title = listing.street || listing.formatted_address || 'Property';
  
  // Create location string
  const location = `${listing.city}, ${listing.state?.toUpperCase()}`;

  // Map status
  let status: Property['status'] = 'Active';
  if (listing.status === 'PENDING' || listing.mls_status === 'Pending') {
    status = 'Pending';
  } else if (listing.status === 'SOLD') {
    status = 'Sold';
  } else if (listing.status === 'FOR_SALE') {
    status = 'Active';
  }

  // Map property type
  let propertyType: Property['type'] = 'House';
  if (listing.style === 'CONDOS') {
    propertyType = 'Condo';
  } else if (listing.style === 'TOWNHOUSE') {
    propertyType = 'Townhouse';
  } else if (listing.style === 'SINGLE_FAMILY') {
    propertyType = 'House';
  }

  // Create price history (mock for now - we'll get real data later)
  const currentPrice = listing.list_price || 0;
  const history = [
    { date: listing.list_date || new Date().toISOString(), price: currentPrice }
  ];
  if (listing.last_sold_price && listing.last_sold_date) {
    history.unshift({
      date: listing.last_sold_date,
      price: listing.last_sold_price
    });
  }

  // Extract features from text description
  const features: string[] = [];
  const text = listing.text?.toLowerCase() || '';
  if (text.includes('pool')) features.push('Pool');
  if (text.includes('garage') || listing.parking_garage) features.push('Garage');
  if (text.includes('fireplace')) features.push('Fireplace');
  if (text.includes('kitchen')) features.push('Modern Kitchen');
  if (listing.new_construction) features.push('New Construction');
  if (text.includes('master') || text.includes('primary')) features.push('Primary Suite');

  return {
    id: listing.property_id,
    title,
    price: currentPrice,
    location,
    street: listing.street,
    city: listing.city,
    state: listing.state?.toUpperCase(),
    zipCode: listing.zip_code,
    sqft: listing.sqft || 0,
    beds: listing.beds || 0,
    baths: totalBaths,
    image: images[0] || 'https://images.unsplash.com/photo-1580587771525-78b9dba3b614?w=1600&h=900&fit=crop',
    description: listing.text || 'No description available.',
    features,
    type: propertyType,
    yearBuilt: listing.year_built || new Date().getFullYear(),
    status,
    history,
    coordinates: {
      lat: listing.latitude || 33.4484, // Phoenix default
      lng: listing.longitude || -112.0740
    },
    propertyUrl: listing.property_url,
    lotSqft: listing.lot_sqft || undefined,
    hoaFee: listing.hoa_fee || undefined,
    agentName: listing.agent_name || undefined,
    officeName: listing.office_name || undefined,
    altPhotos: images.slice(1) // All except primary
  };
}

// Format price for display
export function formatPrice(price: number): string {
  if (price >= 1000000) {
    return `$${(price / 1000000).toFixed(1)}M`;
  } else if (price >= 1000) {
    return `$${(price / 1000).toFixed(0)}K`;
  } else if (price > 0) {
    return `$${price.toLocaleString()}`;
  }
  return 'Price TBD';
}

// Format square footage
export function formatSqft(sqft: number): string {
  if (sqft >= 1000) {
    return `${(sqft / 1000).toFixed(1)}k`;
  } else if (sqft > 0) {
    return sqft.toLocaleString();
  }
  return '-';
}