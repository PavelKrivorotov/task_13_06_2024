"""Insert default values to categories

Revision ID: f3d498706ddf
Revises: 889403a7982c
Create Date: 2024-06-13 19:20:13.593275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3d498706ddf'
down_revision: Union[str, None] = '889403a7982c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.execute("""
        INSERT INTO categories
            (key, title, description)
        VALUES
            ('001', 'Bakery', '...'),
            ('002', 'Fruits & Vegetables', '...'),
            ('003', 'Alcohol', '...'),
            ('004', 'Meat & Sausage', '...'),
            ('005', 'Fish', '...');
    """)
    # ###


def downgrade() -> None:
    # ###
    op.execute('DELETE FROM categories;')
    # ###
