"""
Use case for creating a new transaction.

[Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-BE-T02]
"""
from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import TransactionRepository
from app.application.exceptions.exceptions import CategoryNotFoundError


class CreateTransactionUseCase:
    """
    Use case for creating a new transaction.
    
    Orchestrates the transaction creation process:
    1. Validate category exists
    2. Create transaction via repository
    3. Return created transaction
    """
    
    def __init__(self, repository: TransactionRepository):
        self.repository = repository
    
    def execute(self, transaction: Transaction) -> Transaction:
        """
        Create a new transaction.
        
        Args:
            transaction: Transaction entity to create
            
        Returns:
            Created transaction with id and timestamps
            
        Raises:
            CategoryNotFoundError: If category_id does not exist
        """
        # Validate category exists
        if not self.repository.category_exists(transaction.category_id):
            raise CategoryNotFoundError(f"Category {transaction.category_id} not found")
        
        # Create transaction
        created_transaction = self.repository.create(transaction)
        
        return created_transaction
