from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Project Root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SQLite Database
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'beauty_analyzer.db')}"

print(DATABASE_URL)

# Engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base Class
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()