from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ARRAY, Boolean, JSON
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from ..db.database import Base

class Property(Base):
    __tablename__ = "properties"

    # Primary Key
    id = Column(String, primary_key=True, index=True)
    
    # Basic Info
    title = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    city = Column(String, index=True)
    state = Column(String, index=True)
    zip_code = Column(String, index=True)
    
    # Property Details
    price = Column(Integer, nullable=False, index=True)
    beds = Column(Integer, index=True)
    baths = Column(Float, index=True)
    sqft = Column(Integer, index=True)
    lot_sqft = Column(Integer)
    year_built = Column(Integer, index=True)
    
    # Property Type & Status
    property_type = Column(String, index=True)  # House, Condo, Townhouse, etc.
    status = Column(String, index=True)  # Active, Pending, Sold
    
    # Location (for geospatial queries)
    latitude = Column(Float)
    longitude = Column(Float)
    location = Column(Geometry('POINT', srid=4326))  # PostGIS point
    
    # Additional Details
    description = Column(Text)
    features = Column(ARRAY(String))  # Array of feature strings
    hoa_fee = Column(Integer)
    
    # Images
    image = Column(String)  # Main image URL
    alt_photos = Column(ARRAY(String))  # Additional photos
    
    # Agent Info
    agent_name = Column(String)
    agent_phone = Column(String)
    office_name = Column(String)
    
    # External Links
    property_url = Column(String)
    mls_number = Column(String, index=True)
    
    # Price History (stored as JSON)
    price_history = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Search optimization
    is_featured = Column(Boolean, default=False, index=True)
    
    def __repr__(self):
        return f"<Property {self.id}: {self.title} - ${self.price}>"