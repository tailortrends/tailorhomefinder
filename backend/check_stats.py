from src.app.db.database import SessionLocal
from src.app.models.property import Property
from sqlalchemy import func

db = SessionLocal()

# Total count
total = db.query(Property).count()
print(f"🏠 Total Properties: {total:,}\n")

# By state
by_state = db.query(
    Property.state,
    func.count(Property.id)
).group_by(Property.state).all()

print("📍 Properties by State:")
for state, count in sorted(by_state, key=lambda x: x[1], reverse=True):
    print(f"   {state.upper()}: {count:,}")

# Price stats
avg_price = db.query(func.avg(Property.price)).scalar()
min_price = db.query(func.min(Property.price)).scalar()
max_price = db.query(func.max(Property.price)).scalar()

print(f"\n💰 Price Stats:")
print(f"   Average: ${int(avg_price):,}")
print(f"   Min: ${int(min_price):,}")
print(f"   Max: ${int(max_price):,}")

db.close()
