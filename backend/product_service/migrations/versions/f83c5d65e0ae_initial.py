from typing import Union, Sequence
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum

# revision identifiers, used by Alembic.
revision: str = 'f83c5d65e0ae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Enums
product_category_enum = sa.Enum(
    'ELECTRONICS', 
    'FASHION', 
    'HOME', 
    'BEAUTY', 
    'SPORTS', 
    'TOYS', 
    'BOOKS', 
    'FOOD',
    name='productcategory'
)

def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('name', sa.String, nullable=False, index=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('stock_quantity', sa.Integer, nullable=False, default=1),
        sa.Column('category', product_category_enum, nullable=False),
    )

def downgrade() -> None:
    op.drop_table('products')
    product_category_enum.drop(op.get_bind(), checkfirst=False)