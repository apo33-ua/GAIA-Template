"""
Database configuration and session management.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL from environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://expense_user:expense_pass@database:5432/expense_tracker"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

# Import all models to ensure they are registered with Base.metadata
# This must be done after Base is created
from app.infrastructure.models.user import UserModel  # noqa: E402, F401
from app.infrastructure.models.category import CategoryModel  # noqa: E402, F401
from app.infrastructure.models.transaction import TransactionModel  # noqa: E402, F401


def get_db():
    """
    Dependency function to get database session.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
