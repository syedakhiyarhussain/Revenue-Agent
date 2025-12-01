# database/db_session.py

from sqlmodel import create_engine, SQLModel, Session
from config import settings

# The engine connects to the database specified in config.py
engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    """Initializes the database and creates all tables defined by SQLModel."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency to provide a database session."""
    with Session(engine) as session:
        yield session