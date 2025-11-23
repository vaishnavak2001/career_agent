"""
Drop and recreate all tables - USE WITH CAUTION!
"""
from app.db.session import engine, Base
from app.db.models import User, Resume, Job, Project, Application, ActivityLog

def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully!")

if __name__ == "__main__":
    import sys
    confirm = input("This will DELETE ALL DATA. Type 'YES' to confirm: ")
    if confirm == "YES":
        reset_database()
    else:
        print("Aborted.")
        sys.exit(1)
