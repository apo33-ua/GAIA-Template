"""
Pydantic DTOs for transaction endpoints.

[Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-BE-T02]
"""
from pydantic import BaseModel, Field, field_validator
from datetime import date as date_type, datetime
from decimal import Decimal
from typing import Optional


class CreateTransactionRequest(BaseModel):
    """
    Request DTO for creating a transaction.
    
    Validates:
    - Amount must be positive
    - transaction_date cannot be in the future
    - transaction_type must be 'income' or 'expense'
    """
    transaction_type: str = Field(..., alias="type", description="Transaction type (income or expense)")
    amount: Decimal = Field(..., gt=0, description="Transaction amount (must be positive)")
    transaction_date: date_type = Field(..., alias="date", description="Transaction date")
    category_id: int = Field(..., gt=0, description="Category ID")
    description: Optional[str] = Field(None, max_length=500, description="Optional description")
    
    @field_validator("transaction_type")
    @classmethod
    def validate_transaction_type(cls, v: str) -> str:
        if v not in ("income", "expense"):
            raise ValueError("Type must be 'income' or 'expense'")
        return v
    
    @field_validator("transaction_date")
    @classmethod
    def date_not_in_future(cls, v: date_type) -> date_type:
        if v > datetime.now().date():
            raise ValueError("Date cannot be in the future")
        return v
    
    model_config = {
        "extra": "forbid",  # Reject unexpected fields (Mass Assignment prevention)
        "populate_by_name": True,  # Allow both 'type' and 'transaction_type', 'date' and 'transaction_date'
        "json_schema_extra": {
            "examples": [
                {
                    "type": "expense",
                    "amount": "45.50",
                    "date": "2026-02-03",
                    "category_id": 1,
                    "description": "Lunch at restaurant"
                }
            ]
        }
    }


class TransactionResponse(BaseModel):
    """
    Response DTO for transaction.
    
    Includes category name for convenience (joined from categories table).
    """
    id: int
    user_id: int
    transaction_type: str = Field(..., alias="type")
    amount: Decimal
    transaction_date: date_type = Field(..., alias="date")
    category_id: int
    category_name: str  # Joined from categories table
    description: Optional[str]
    created_at: datetime
    
    model_config = {
        "from_attributes": True,  # Enable ORM mode
        "populate_by_name": True,  # Allow both 'type' and 'transaction_type', 'date' and 'transaction_date'
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "user_id": 123,
                    "type": "expense",
                    "amount": "45.50",
                    "date": "2026-02-03",
                    "category_id": 1,
                    "category_name": "Food",
                    "description": "Lunch at restaurant",
                    "created_at": "2026-02-03T12:30:00Z"
                }
            ]
        }
    }
