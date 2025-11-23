from app.db.session import engine, Base
from app.db.models import User, Job, Resume, Project, Application, ActivityLog

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_db()
