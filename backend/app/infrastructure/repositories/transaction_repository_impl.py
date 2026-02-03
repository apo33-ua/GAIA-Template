"""
SQLAlchemy implementation of TransactionRepository.

[Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-BE-T02]
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import TransactionRepository
from app.infrastructure.models.transaction import TransactionModel
from app.infrastructure.models.category import CategoryModel
from app.application.exceptions.exceptions import DatabaseError


class TransactionRepositoryImpl(TransactionRepository):
    """
    SQLAlchemy implementation of TransactionRepository.
    
    This is an adapter in Clean Architecture - implements the port
    defined in the domain layer.
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, transaction: Transaction) -> Transaction:
        """Create a new transaction."""
        model = TransactionModel(
            user_id=transaction.user_id,
            type=transaction.type,
            amount=transaction.amount,
            date=transaction.date,
            category_id=transaction.category_id,
            description=transaction.description,
        )
        
        try:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
        except IntegrityError as e:
            self.session.rollback()
            raise DatabaseError(f"Failed to create transaction: {e}")
        
        # Convert model to entity
        return Transaction(
            id=model.id,
            user_id=model.user_id,
            type=model.type,
            amount=model.amount,
            date=model.date,
            category_id=model.category_id,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def category_exists(self, category_id: int) -> bool:
        """Check if a category exists."""
        return self.session.query(CategoryModel).filter(CategoryModel.id == category_id).first() is not None
