"""create transactions and categories tables

Revision ID: b6db15062087
Revises: 001
Create Date: 2026-02-03 21:23:00.000000

[Feature: Personal Expense Management] [Story: PEM-USER-001] [Ticket: PEM-USER-001-DB-T01]
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6db15062087'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create categories and transactions tables for Personal Expense Management.
    
    PII SECURITY: amount and description fields contain sensitive financial data.
    Ensure database encryption at rest is enabled at infrastructure level.
    """
    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('type', sa.String(20), nullable=False),
        sa.CheckConstraint("type IN ('expense', 'income')", name='check_category_type')
    )
    
    # Create transactions table
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(20), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_transactions_user_id'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name='fk_transactions_category_id'),
        sa.CheckConstraint('amount > 0', name='check_amount_positive'),
        sa.CheckConstraint("type IN ('income', 'expense')", name='check_transaction_type')
    )
    
    # Add performance indexes
    op.create_index(
        'idx_transactions_user_date',
        'transactions',
        ['user_id', 'date']
    )
    op.create_index(
        'idx_transactions_user_category',
        'transactions',
        ['user_id', 'category_id']
    )
    
    # Seed predefined expense categories
    from sqlalchemy import table, column, String
    
    categories_table = table(
        'categories',
        column('name', String),
        column('type', String)
    )
    
    op.bulk_insert(categories_table, [
        {'name': 'Food', 'type': 'expense'},
        {'name': 'Transportation', 'type': 'expense'},
        {'name': 'Entertainment', 'type': 'expense'},
        {'name': 'Utilities', 'type': 'expense'},
        {'name': 'Health', 'type': 'expense'},
        {'name': 'Other', 'type': 'expense'},
    ])


def downgrade() -> None:
    """Drop transactions and categories tables."""
    # Drop indexes first
    op.drop_index('idx_transactions_user_category', table_name='transactions')
    op.drop_index('idx_transactions_user_date', table_name='transactions')
    
    # Drop transactions table (foreign keys will be dropped automatically)
    op.drop_table('transactions')
    
    # Drop categories table
    op.drop_table('categories')
