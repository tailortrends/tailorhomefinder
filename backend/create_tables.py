"""
Script to create database tables for TailorHomeFinder.
Run this after setting up the database to create any missing tables.
"""
import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv
load_dotenv()

from app.db.database import engine, Base
from app.models.property import Property
from app.models.inquiry import Inquiry

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")

    # Import all models to ensure they're registered with Base
    from app.models import Property, Inquiry

    # Create all tables
    Base.metadata.create_all(bind=engine)

    print("Tables created successfully!")
    print("\nCreated tables:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")

if __name__ == "__main__":
    create_tables()
