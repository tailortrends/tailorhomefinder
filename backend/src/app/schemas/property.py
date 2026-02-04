from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PropertyBase(BaseModel):
    title: str
    address: str
    city: str
    state: str
    zip_code: str
    price: int
    beds: Optional[int] = None
    baths: Optional[float] = None
    sqft: Optional[int] = None
    lot_sqft: Optional[int] = None
    year_built: Optional[int] = None
    property_type: str
    status: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    features: Optional[List[str]] = []
    hoa_fee: Optional[int] = None
    image: Optional[str] = None
    alt_photos: Optional[List[str]] = []
    agent_name: Optional[str] = None
    agent_phone: Optional[str] = None
    office_name: Optional[str] = None
    property_url: Optional[str] = None
    mls_number: Optional[str] = None
    price_history: Optional[List[dict]] = []
    is_featured: bool = False

class PropertyCreate(PropertyBase):
    id: str

class PropertyResponse(PropertyBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PropertySearch(BaseModel):
    query: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    beds: Optional[int] = None
    baths: Optional[float] = None
    min_sqft: Optional[int] = None
    max_sqft: Optional[int] = None
    property_type: Optional[str] = None
    status: Optional[str] = None
    limit: int = Field(default=20, le=100)
    offset: int = 0

class PropertyList(BaseModel):
    total: int
    properties: List[PropertyResponse]
    limit: int
    offset: int
