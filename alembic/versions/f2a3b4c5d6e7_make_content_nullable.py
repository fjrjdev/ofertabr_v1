"""make content nullable

Revision ID: f2a3b4c5d6e7
Revises: ea6d517c2e95
Create Date: 2025-10-26 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2a3b4c5d6e7'
down_revision = 'ea6d517c2e95'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Tornar o campo 'content' nullable
    op.alter_column('scraped_content', 'content',
               existing_type=sa.Text(),
               nullable=True)


def downgrade() -> None:
    # Reverter: tornar o campo 'content' obrigatório novamente
    op.alter_column('scraped_content', 'content',
               existing_type=sa.Text(),
               nullable=False)

