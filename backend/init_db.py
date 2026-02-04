from src.app.db.database import engine, Base
# Import models to register them with Base
from src.app.models.property import Property

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Done!")
