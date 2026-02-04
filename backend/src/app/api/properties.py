from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import Optional
from ..db.database import get_db
from ..models.property import Property
from ..schemas.property import PropertyResponse, PropertyList

router = APIRouter(prefix="/api/properties", tags=["Properties"])

@router.get("/", response_model=PropertyList)
async def get_properties(
    city: Optional[str] = None,
    state: Optional[str] = None,
    zip_code: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    beds: Optional[int] = None,
    baths: Optional[float] = None,
    property_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(default=20, le=100),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Property)
    filters = []
    
    if city:
        filters.append(Property.city.ilike(f"%{city}%"))
    if state:
        filters.append(Property.state == state)
    if zip_code:
        filters.append(Property.zip_code == zip_code)
    if min_price:
        filters.append(Property.price >= min_price)
    if max_price:
        filters.append(Property.price <= max_price)
    if beds:
        filters.append(Property.beds >= beds)
    if baths:
        filters.append(Property.baths >= baths)
    if property_type:
        filters.append(Property.property_type == property_type)
    if status:
        filters.append(Property.status == status)
    
    if filters:
        query = query.filter(and_(*filters))
    
    total = query.count()
    properties = query.order_by(Property.created_at.desc()).offset(offset).limit(limit).all()
    
    return PropertyList(total=total, properties=properties, limit=limit, offset=offset)

@router.get("/stats/overview")
async def get_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Property.id)).scalar() or 0
    avg_price = db.query(func.avg(Property.price)).scalar()

    return {
        "total_properties": total,
        "avg_price": int(avg_price) if avg_price else 0
    }

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(property_id: str, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property
