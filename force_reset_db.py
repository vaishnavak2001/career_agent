"""
Drop all tables with CASCADE - forceful reset
"""
from sqlalchemy import text
from app.db.session import engine

def force_reset():
    print("Force dropping all tables with CASCADE...")
    with engine.connect() as conn:
        # Drop all tables in public schema
        result = conn.execute(text("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """))
        conn.commit()
    
    print("Creating new tables...")
    from app.db.session import Base
    from app.db.models import User, Resume, Job, Project, Application, ActivityLog
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully!")

if __name__ == "__main__":
    force_reset()
