"""
FastAPI router for transactions endpoints.

[Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-BE-T02]
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user_id
from app.presentation.schemas.transaction import CreateTransactionRequest, TransactionResponse
from app.application.use_cases.create_transaction import CreateTransactionUseCase
from app.infrastructure.repositories.transaction_repository_impl import TransactionRepositoryImpl
from app.domain.entities.transaction import Transaction
from app.application.exceptions.exceptions import CategoryNotFoundError
import logging
import uuid

router = APIRouter(prefix="/api/transactions", tags=["transactions"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    request: CreateTransactionRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Create a new transaction.
    
    [Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-BE-T02]
    
    Scenarios covered:
    - PEM-USER-001 Scenario 1: Successfully add expense with all required fields
    - PEM-USER-001 Scenario 2: Add expense with optional description
    - PEM-USER-001 Scenario 3-6: Validation errors (handled by Pydantic)
    - PEM-USER-001 Scenario 7: Authorization enforcement (user_id from JWT)
    - PEM-USER-001 Scenario 10: Error handling for server failure
    
    Args:
        request: Transaction creation request
        user_id: Authenticated user ID (from JWT/header)
        db: Database session
        
    Returns:
        Created transaction with category name
        
    Raises:
        400: Validation error or category not found
        401: Unauthorized (missing/invalid auth)
        500: Server error
    """
    correlation_id = str(uuid.uuid4())
    
    try:
        # Create domain entity (NEVER trust user_id from request body - BOLA prevention)
        transaction = Transaction(
            user_id=user_id,  # From JWT/header (BOLA prevention)
            type=request.transaction_type,
            amount=request.amount,
            date=request.transaction_date,
            category_id=request.category_id,
            description=request.description,
        )
        
        # Execute use case
        repository = TransactionRepositoryImpl(db)
        use_case = CreateTransactionUseCase(repository)
        created_transaction = use_case.execute(transaction)
        
        # Fetch category name for response
        from app.infrastructure.models.category import CategoryModel
        category = db.query(CategoryModel).filter(CategoryModel.id == created_transaction.category_id).first()
        
        # Log success (INFO level, no PII)
        logger.info(
            f"Transaction created successfully",
            extra={
                "correlation_id": correlation_id,
                "user_id": user_id,
                "category_id": created_transaction.category_id,
                "transaction_id": created_transaction.id,
            }
        )
        
        # Build response
        response = TransactionResponse(
            id=created_transaction.id,
            user_id=created_transaction.user_id,
            transaction_type=created_transaction.type,
            amount=created_transaction.amount,
            transaction_date=created_transaction.date,
            category_id=created_transaction.category_id,
            category_name=category.name if category else "Unknown",
            description=created_transaction.description,
            created_at=created_transaction.created_at,
        )
        
        return response
        
    except CategoryNotFoundError as e:
        # Log validation error (WARN level)
        logger.warning(
            f"Category not found",
            extra={
                "correlation_id": correlation_id,
                "category_id": request.category_id,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except ValueError as e:
        # Business rule validation error
        logger.warning(
            f"Validation error",
            extra={
                "correlation_id": correlation_id,
                "error": str(e),
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        # Server error (ERROR level)
        logger.error(
            f"Failed to create transaction",
            extra={
                "correlation_id": correlation_id,
                "error_type": type(e).__name__,
            },
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
