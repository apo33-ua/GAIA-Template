"""
Application layer exceptions.

[Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-BE-T02]
"""


class CategoryNotFoundError(Exception):
    """Raised when a category ID does not exist."""
    pass


class DatabaseError(Exception):
    """Raised when a database operation fails."""
    pass
