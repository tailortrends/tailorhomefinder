import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    print("✅ PostgreSQL connection successful!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"📊 PostgreSQL version: {version[0]}")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
