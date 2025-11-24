"""Initialize database tables."""
from app.database import engine, Base
from app.models import (
    User, Job, Resume, Project, 
    CoverLetter, Application, DailyMetric, JobStatus
)


def init_db():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    
    # Print created tables
    print("\nCreated tables:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")


if __name__ == "__main__":
    init_db()
