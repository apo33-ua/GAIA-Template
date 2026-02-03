"""
Domain entity representing a financial transaction.

[Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-BE-T02]
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Optional


class Transaction:
    """
    Domain entity representing a financial transaction.
    
    Business Rules:
    - Amount must be positive
    - Type must be 'income' or 'expense'
    - Date cannot be in the future
    """
    
    def __init__(
        self,
        user_id: int,
        type: Literal["income", "expense"],
        amount: Decimal,
        date: date,
        category_id: int,
        description: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        # Business rule: amount must be positive
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Business rule: type must be income or expense
        if type not in ("income", "expense"):
            raise ValueError("Type must be 'income' or 'expense'")
        
        # Business rule: date cannot be in the future
        if date > datetime.now().date():
            raise ValueError("Date cannot be in the future")
        
        self.id = id
        self.user_id = user_id
        self.type = type
        self.amount = amount
        self.date = date
        self.category_id = category_id
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
