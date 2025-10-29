"""add_product_fields_to_scraped_content

Revision ID: ea6d517c2e95
Revises: 0f10c25e5424
Create Date: 2025-10-26 12:51:36.360832

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ea6d517c2e95'
down_revision: str | Sequence[str] | None = '0f10c25e5424'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add product-specific fields to scraped_content table
    op.add_column('scraped_content', sa.Column('product_url', sa.String(1000), nullable=True))
    op.add_column('scraped_content', sa.Column('current_price', sa.Numeric(10, 2), nullable=True))
    op.add_column('scraped_content', sa.Column('original_price', sa.Numeric(10, 2), nullable=True))
    op.add_column('scraped_content', sa.Column('discount_percentage', sa.Numeric(5, 2), nullable=True))
    op.add_column('scraped_content', sa.Column('installments', sa.String(200), nullable=True))
    op.add_column('scraped_content', sa.Column('free_shipping', sa.Boolean(), default=False))
    op.add_column('scraped_content', sa.Column('store_name', sa.String(100), nullable=True))
    op.add_column('scraped_content', sa.Column('category', sa.String(100), nullable=True))
    op.add_column('scraped_content', sa.Column('rating', sa.Numeric(3, 2), nullable=True))
    op.add_column('scraped_content', sa.Column('reviews_count', sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove product-specific fields from scraped_content table
    op.drop_column('scraped_content', 'reviews_count')
    op.drop_column('scraped_content', 'rating')
    op.drop_column('scraped_content', 'category')
    op.drop_column('scraped_content', 'store_name')
    op.drop_column('scraped_content', 'free_shipping')
    op.drop_column('scraped_content', 'installments')
    op.drop_column('scraped_content', 'discount_percentage')
    op.drop_column('scraped_content', 'original_price')
    op.drop_column('scraped_content', 'current_price')
    op.drop_column('scraped_content', 'product_url')
