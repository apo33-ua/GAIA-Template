"""
SQLAlchemy model for categories table.

[Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-BE-T02]
"""
from sqlalchemy import Column, Integer, String, CheckConstraint
from app.core.database import Base


class CategoryModel(Base):
    """
    SQLAlchemy model for categories table.
    
    Maps to the categories table created in PEM-USER-001-DB-T01.
    """
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    type = Column(String(20), nullable=False)
    
    __table_args__ = (
        CheckConstraint("type IN ('expense', 'income')", name="check_category_type"),
    )
