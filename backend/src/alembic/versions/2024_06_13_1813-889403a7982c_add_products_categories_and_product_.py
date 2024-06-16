"""Add products, categories and product_category tables

Revision ID: 889403a7982c
Revises: 
Create Date: 2024-06-13 18:13:14.649233

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa

from categories.utils import gen_category_key


# revision identifiers, used by Alembic.
revision: str = '889403a7982c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.create_table(
        'products',
        sa.Column('id', sa.Uuid(), primary_key=True, default=uuid.uuid4),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('price', sa.Numeric(8, 2), nullable=False),
        sa.Column('published', sa.DateTime(), index=True, server_default=sa.func.now(), nullable=False,)
    )

    op.create_table(
        'categories',
        sa.Column('key', sa.String(8), primary_key=True, default=gen_category_key),
        sa.Column('title', sa.String(255), index=True, unique=True, nullable=False),
        sa.Column('description', sa.Text())
    )

    op.create_table(
        'product_category',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('product_id', sa.Uuid(), sa.ForeignKey('products.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('category_key', sa.String(8), sa.ForeignKey('categories.key', ondelete='CASCADE'), index=True, nullable=False)
    )
    # ###


def downgrade() -> None:
    # ###
    op.drop_table('product_category')
    op.drop_table('categories')
    op.drop_table('products')
    # ###
