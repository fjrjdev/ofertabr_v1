"""remove admins table

Revision ID: a1b2c3d4e5f6
Revises: f2a3b4c5d6e7
Create Date: 2025-10-27 00:00:00.000000

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'f2a3b4c5d6e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Remove admins table - not needed with passwordless auth"""
    # Drop indexes first
    op.drop_index('ix_admins_username', table_name='admins')
    op.drop_index('ix_admins_email', table_name='admins')

    # Drop table
    op.drop_table('admins')


def downgrade() -> None:
    """Recreate admins table if needed"""
    op.create_table('admins',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(length=128), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_admins_email', 'admins', ['email'], unique=True)
    op.create_index('ix_admins_username', 'admins', ['username'], unique=True)

