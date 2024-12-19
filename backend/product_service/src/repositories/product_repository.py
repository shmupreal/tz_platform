from fastapi import HTTPException
from ..enums.product_category import ProductCategory
from sqlalchemy import select
from typing import Optional, List
from ..models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_products(self) -> List[Product]:
        result = await self.db.execute(select(Product))
        return result.scalars().all()

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        result = await self.db.execute(select(Product).filter(Product.id == product_id))
        return result.scalar_one_or_none()
    
    async def get_products_by_category(self, category: ProductCategory) -> List[Product]:
        result = await self.db.execute(select(Product).filter(Product.category == category))
        return result.scalars().all()  

    async def create_product(self, product_data: dict) -> Product:
        try:
            new_product = Product(**product_data) 
            self.db.add(new_product)
            await self.db.commit()
            await self.db.refresh(new_product) 
            return new_product
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")
    
    async def update_product(self, product_id: int, updated_data: dict) -> Optional[Product]:
        product = await self.get_product_by_id(product_id)
        if not product:
            return None
        for key, value in updated_data.items():
            setattr(product, key, value)
        await self.db.commit()
        await self.db.refresh(product)
        return product
    
    async def delete_product(self, product_id: int) -> bool:
        product = await self.get_product_by_id(product_id)
        if not product:
            return False
        await self.db.delete(product)
        await self.db.commit()
        return True
