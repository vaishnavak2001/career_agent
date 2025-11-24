"""Drop all existing tables and recreate them."""
from sqlalchemy import text
from app.database import engine, Base, SessionLocal
from app.models import (
    User, Job, Resume, Project,
    CoverLetter, Application, DailyMetric
)

def reset_database():
    """Drop all tables and recreate them."""
    print("\n[RESET] Dropping all existing tables...")
    
    try:
        # Drop all tables with CASCADE to handle dependencies
        with engine.connect() as conn:
            # Get all table names
            result = conn.execute(text("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
            """))
            tables = [row[0] for row in result]
            
            if tables:
                print(f"[INFO] Found {len(tables)} tables to drop")
                for table in tables:
                    print(f"  - {table}")
                
                # Drop each table with CASCADE
                for table in tables:
                    conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                    conn.commit()
                    
                print("[SUCCESS] All tables dropped")
            else:
                print("[INFO] No tables found (fresh database)")
                
    except Exception as e:
        print(f"[WARNING] Drop failed: {e}")
        # Try using SQLAlchemy's drop_all as fallback
        try:
            Base.metadata.drop_all(bind=engine)
            print("[SUCCESS] Tables dropped using metadata")
        except Exception as e2:
            print(f"[ERROR] Both drop methods failed: {e2}")

    
    print("\n[RESET] Creating fresh tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("[SUCCESS] All tables created")
        
        # List created tables
        print("\n[INFO] Created tables:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
            
    except Exception as e:
        print(f"[ERROR] Table creation failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE RESET UTILITY")
    print("=" * 60)
    print("\nThis will DROP all tables and recreate them.")
    print("All existing data will be LOST!")
    print("\n" + "=" * 60)
    
    response = input("\nContinue? (yes/no): ").strip().lower()
    
    if response == "yes":
        success = reset_database()
        if success:
            print("\n[SUCCESS] Database reset complete!")
        else:
            print("\n[ERROR] Database reset failed!")
    else:
        print("\n[CANCELLED] Database reset cancelled.")
