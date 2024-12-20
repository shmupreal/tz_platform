from ...enums.product_category import ProductCategory
from typing import List, Optional
from fastapi import Query
from ...api.deps.product_deps import get_product_service, get_current_user
from ...api.schemas.product import ProductResponseDTO, ProductUpdateDTO, ProductCreateDTO
from fastapi import APIRouter, Depends, HTTPException
from ...services.product_service import ProductService
from fastapi_cache.decorator import cache

product_router = APIRouter(
    prefix="/product",
    tags=["Products"]
)

@product_router.get("/", response_model=List[ProductResponseDTO])
@cache(expire=180)
async def get_all_products(
    product_service: ProductService = Depends(get_product_service)
) -> List[ProductResponseDTO]:
    products = await product_service.get_products()
    return products

@product_router.get("/{product_id}", response_model=ProductResponseDTO)
async def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)  
):
    product = await product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@product_router.get("/category/{category}", response_model=List[ProductResponseDTO])
async def get_products_by_category(
    category: ProductCategory,
    product_service: ProductService = Depends(get_product_service)
) -> List[ProductResponseDTO]:
    products = await product_service.get_products_by_category(category)
    if not products:
        raise HTTPException(status_code=404, detail="Products by this category not found")
    return [ProductResponseDTO.model_validate(product) for product in products]

@product_router.post("/", response_model=ProductResponseDTO)
async def create_product(
    product_data: ProductCreateDTO,
    current_user: dict = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service)
) -> ProductResponseDTO:
    return await product_service.create_product(product_data, user_id=current_user["id"])

@product_router.put("/{product_id}", response_model=ProductResponseDTO)
async def update_product(
    product_id: int,
    product_data: ProductUpdateDTO,
    product_service: ProductService = Depends(get_product_service)
) -> ProductResponseDTO:
    updated_product = await product_service.update_product(product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@product_router.delete("/{product_id}", response_model=bool)
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)
) -> bool:
    result = await product_service.delete_product(product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

@product_router.get("/filter/", response_model=List[ProductResponseDTO])
async def filter_products(
    name: Optional[str] = Query(None, description="Filter by product name"),
    description: Optional[str] = Query(None, description="Filter by product description"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    category: Optional[ProductCategory] = Query(None, description="Product category"),
    product_service: ProductService = Depends(get_product_service),
) -> List[ProductResponseDTO]:
    return await product_service.filter_products(
        name=name,
        description=description,
        min_price=min_price,
        max_price=max_price,
        category=category,
    )