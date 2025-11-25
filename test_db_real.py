import os
import sys
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Load from .env manually to be sure
from dotenv import load_dotenv
load_dotenv()

database_url = os.getenv("DATABASE_URL")
print(f"Testing connection to: {database_url.split('@')[1] if '@' in database_url else 'LOCAL'}")

try:
    engine = create_engine(database_url)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection successful!", result.fetchone())
except Exception as e:
    print(f"Connection failed: {e}")
