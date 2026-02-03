"""
SQLAlchemy model for users table.

[Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-BE-T02]
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class UserModel(Base):
    """
    SQLAlchemy model for users table.
    
    Maps to the users table created in the initial migration.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
