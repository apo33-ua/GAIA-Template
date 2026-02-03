"""
Repository interface for Transaction entity (Port).

[Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-BE-T02]
"""
from abc import ABC, abstractmethod
from app.domain.entities.transaction import Transaction


class TransactionRepository(ABC):
    """
    Repository interface for Transaction entity.
    
    This is a port in Clean Architecture - defines the contract
    that infrastructure adapters must implement.
    """
    
    @abstractmethod
    def create(self, transaction: Transaction) -> Transaction:
        """
        Create a new transaction.
        
        Args:
            transaction: Transaction entity to persist
            
        Returns:
            Transaction entity with id and timestamps populated
            
        Raises:
            CategoryNotFoundError: If category_id does not exist
            DatabaseError: If database operation fails
        """
        pass
    
    @abstractmethod
    def category_exists(self, category_id: int) -> bool:
        """
        Check if a category exists.
        
        Args:
            category_id: Category ID to check
            
        Returns:
            True if category exists, False otherwise
        """
        pass
