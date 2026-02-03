"""
Authentication utilities (simplified for MVP).

[Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-BE-T02]

NOTE: This is a simplified implementation for MVP.
In production, this should use proper JWT validation.
"""
from fastapi import Header, HTTPException, status


def get_current_user_id(x_user_id: int = Header(..., description="User ID (from JWT in production)")) -> int:
    """
    Extract user ID from request headers.
    
    SIMPLIFIED FOR MVP: In production, this should:
    1. Extract JWT from Authorization header
    2. Validate JWT signature
    3. Extract user_id from JWT claims
    
    For now, we accept user_id from X-User-Id header for testing.
    
    Args:
        x_user_id: User ID from X-User-Id header
        
    Returns:
        User ID
        
    Raises:
        HTTPException: If user_id is missing or invalid
    """
    if x_user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID"
        )
    return x_user_id
