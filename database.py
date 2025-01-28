from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # Update this to your actual database URL

# Create an engine instance
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for the models
Base = declarative_base()

# Function to get a new session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a session object that can be used throughout the app
session = SessionLocal()
