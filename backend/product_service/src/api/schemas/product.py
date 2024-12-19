from pydantic import Field
from typing import Optional
from ...enums.product_category import ProductCategory
from .base import BaseResponse


class ProductBase(BaseResponse):
    name: str
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)
    category: ProductCategory

class ProductCreateDTO(ProductBase):
    ...

class ProductUpdateDTO(BaseResponse):
    name: Optional[str]
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    category: Optional[ProductCategory]

class ProductResponseDTO(ProductBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
