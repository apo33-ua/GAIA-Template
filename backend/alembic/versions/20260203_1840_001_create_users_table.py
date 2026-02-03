"""create users table

Revision ID: 001
Revises: 
Create Date: 2026-02-03 18:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create users table - prerequisite for transactions feature.
    This is a minimal implementation for authentication.
    """
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    
    # Add index on email for faster lookups
    op.create_index('idx_users_email', 'users', ['email'])


def downgrade() -> None:
    """Drop users table."""
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
