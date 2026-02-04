import json
import os
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.app.db.database import SessionLocal, engine
from src.app.models.property import Property, Base
from dotenv import load_dotenv
import hashlib
from datetime import datetime
import uuid

load_dotenv()

def generate_property_id(data):
    """Generate unique ID from multiple property fields with fallback"""
    # Try to use available unique identifiers first
    if data.get('mls_id'):
        return hashlib.md5(str(data.get('mls_id')).encode()).hexdigest()[:16]
    
    # Use combination of fields with random fallback
    unique_parts = [
        str(data.get('street_address', '')),
        str(data.get('city', '')),
        str(data.get('zip_code', '')),
        str(data.get('latitude', '')),
        str(data.get('longitude', '')),
        str(data.get('property_url', '')),
    ]
    
    unique_string = '-'.join(unique_parts).lower()
    
    # If string is too generic, add random component
    if not any(unique_parts[:3]):  # No address, city, or zip
        unique_string += '-' + str(uuid.uuid4())[:8]
    
    return hashlib.md5(unique_string.encode()).hexdigest()[:16]

def convert_home_harvest_to_property(data, file_path):
    """Convert HomeHarvest JSON format to our Property model"""
    try:
        property_id = generate_property_id(data)
        
        street = data.get('street_address', '')
        title = f"{street}" if street else "Property"
        
        price = data.get('list_price', 0)
        if isinstance(price, str):
            price = int(price.replace('$', '').replace(',', ''))
        
        property_data = {
            'id': property_id,
            'title': title,
            'address': street,
            'city': data.get('city', ''),
            'state': data.get('state', ''),
            'zip_code': data.get('zip_code', ''),
            'price': int(price) if price else 0,
            'beds': data.get('beds'),
            'baths': data.get('full_baths'),
            'sqft': data.get('sqft'),
            'lot_sqft': data.get('lot_sqft'),
            'year_built': data.get('year_built'),
            'property_type': data.get('property_type', 'House'),
            'status': data.get('status', 'Active'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'description': data.get('text', ''),
            'hoa_fee': data.get('hoa_fee'),
            'image': data.get('primary_photo'),
            'alt_photos': data.get('photos', [])[:10] if data.get('photos') else [],
            'agent_name': data.get('agent', {}).get('name') if isinstance(data.get('agent'), dict) else None,
            'property_url': data.get('property_url'),
            'mls_number': data.get('mls_id'),
        }
        
        return Property(**property_data)
    except Exception as e:
        return None

def load_all_properties(data_path: str, db: Session, batch_size: int = 500):
    """Load ALL properties with proper error handling"""
    states_dir = Path(data_path) / 'states'
    
    if not states_dir.exists():
        print(f"❌ States directory not found: {states_dir}")
        return 0
    
    print(f"📂 Loading ALL properties from: {states_dir}")
    start_time = datetime.now()
    
    total_loaded = 0
    total_skipped = 0
    total_files = 0
    batch = []
    
    for state_dir in states_dir.iterdir():
        if not state_dir.is_dir() or state_dir.name.startswith('.'):
            continue
            
        state_name = state_dir.name
        zip_files = [f for f in state_dir.glob('*.json') if not f.name.startswith('.')]
        
        print(f"\n📍 {state_name.upper()}: {len(zip_files)} zip codes")
        
        for idx, zip_file in enumerate(zip_files, 1):
            total_files += 1
            
            try:
                with open(zip_file, 'r') as f:
                    properties_data = json.load(f)
                
                if not isinstance(properties_data, list):
                    properties_data = [properties_data]
                
                for prop_data in properties_data:
                    property_obj = convert_home_harvest_to_property(prop_data, zip_file)
                    
                    if property_obj and property_obj.price > 0:
                        # Check if exists using raw SQL for speed
                        exists = db.execute(
                            text("SELECT 1 FROM properties WHERE id = :id LIMIT 1"),
                            {"id": property_obj.id}
                        ).first()
                        
                        if not exists:
                            batch.append(property_obj)
                        else:
                            total_skipped += 1
                        
                        # Commit smaller batches to avoid huge transactions
                        if len(batch) >= batch_size:
                            try:
                                db.add_all(batch)
                                db.commit()
                                total_loaded += len(batch)
                                print(f"   💾 Batch committed: {total_loaded:,} properties | Skipped: {total_skipped:,}")
                                batch = []
                            except Exception as e:
                                print(f"   ⚠️  Batch error, rolling back: {str(e)[:100]}")
                                db.rollback()
                                batch = []
                
                # Progress update every 50 files
                if idx % 50 == 0:
                    print(f"   ⏳ {idx}/{len(zip_files)} files | {total_loaded:,} loaded | {total_skipped:,} skipped")
                
            except Exception as e:
                print(f"   ⚠️  File error in {zip_file.name}")
                continue
        
        # Commit remaining batch for this state
        if batch:
            try:
                db.add_all(batch)
                db.commit()
                total_loaded += len(batch)
                print(f"   ✅ {state_name.upper()} complete: {total_loaded:,} total")
                batch = []
            except Exception as e:
                print(f"   ⚠️  Final batch error: {str(e)[:100]}")
                db.rollback()
    
    elapsed = datetime.now() - start_time
    print(f"\n{'='*60}")
    print(f"✅ Import Complete!")
    print(f"📊 Total Properties Loaded: {total_loaded:,}")
    print(f"⏭️  Skipped (duplicates): {total_skipped:,}")
    print(f"📁 Files Processed: {total_files:,}")
    print(f"⏱️  Time Elapsed: {elapsed}")
    print(f"{'='*60}")
    
    return total_loaded

if __name__ == "__main__":
    print("🚀 Tailor Home Finder - FULL DATA IMPORT v2")
    print("=" * 60)
    print("⚠️  This will import ALL remaining property data!")
    print("=" * 60)
    
    confirm = input("\n👉 Type 'YES' to proceed: ")
    if confirm.upper() != 'YES':
        print("❌ Import cancelled.")
        exit()
    
    print("\n📊 Ensuring database tables exist...")
    Base.metadata.create_all(bind=engine)
    
    data_path = os.getenv('DATA_PATH', '/Users/shyamway/Desktop/Projects/homefinder/data')
    db = SessionLocal()
    
    try:
        current_count = db.query(Property).count()
        print(f"📈 Current properties in database: {current_count:,}")
        
        print(f"\n🔄 Starting FULL import...")
        loaded = load_all_properties(data_path, db, batch_size=500)
        
        final_count = db.query(Property).count()
        print(f"\n🎉 Final database count: {final_count:,} properties!")
        
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        db.rollback()
    finally:
        db.close()