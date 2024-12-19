from ..db.session import Base
from sqlalchemy import (
    Column, String,
    Integer,
    Float,
    Text,
    Enum as SQLAlchemyEnum,
)
from ..enums.product_category import ProductCategory


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=1)
    category = Column(SQLAlchemyEnum(ProductCategory), nullable=False)