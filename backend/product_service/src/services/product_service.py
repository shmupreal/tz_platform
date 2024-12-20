from fastapi import HTTPException
from ..api.schemas.product import ProductCreateDTO, ProductUpdateDTO, ProductResponseDTO
from ..enums.product_category import ProductCategory
from typing import Optional, List
from ..models.product import Product
from ..repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def get_products(self) -> List[Product]:
        return await self.product_repo.get_all_products()
        
    async def get_product(self, product_id: int) -> Optional[Product]:
        return await self.product_repo.get_product_by_id(product_id)
    
    async def get_products_by_category(self, category: ProductCategory) -> List[Product]:
        return await self.product_repo.get_products_by_category(category)
    
    async def create_product(self, product_data: ProductCreateDTO, user_id: int) -> ProductResponseDTO:
        try:
            product_data_dict = product_data.model_dump()
            product_data_dict["user_id"] = user_id

            new_product = await self.product_repo.create_product(product_data_dict)

            return ProductResponseDTO(
                id=new_product.id,
                name=new_product.name,
                description=new_product.description,
                price=new_product.price,
                stock_quantity=new_product.stock_quantity,
                category=new_product.category,
                user_id=new_product.user_id,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

    async def update_product(self, product_id: int, product_data: ProductUpdateDTO) -> Optional[Product]:
        return await self.product_repo.update_product(product_id, product_data.model_dump(exclude_unset=True))
    
    async def delete_product(self, product_id: int) -> bool:
        return await self.product_repo.delete_product(product_id)
    
    async def filter_products(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None,
            category: Optional[ProductCategory] = None,
        ) -> List[ProductResponseDTO]:
            products = await self.product_repo.filter_products(
                name=name,
                description=description,
                min_price=min_price,
                max_price=max_price,
                category=category,
            )
            return [
                ProductResponseDTO(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    stock_quantity=product.stock_quantity,
                    category=product.category,
                    user_id=product.user_id,
                )
                for product in products
            ]