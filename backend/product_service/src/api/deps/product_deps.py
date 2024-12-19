from ...repositories.product_repository import ProductRepository
from ...services.product_service import ProductService
from sqlalchemy.ext.asyncio import AsyncSession
from .session_deps import get_async_session
from fastapi import Depends, HTTPException
from ...utils.user import verify_user

async def get_product_repository(session: AsyncSession = Depends(get_async_session)) -> ProductRepository:
    try:
        return ProductRepository(session)   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing ProductRepository: {str(e)}")

async def get_product_service(product_repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    try:
        return ProductService(product_repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing ProductService: {str(e)}")

async def get_current_user(user: dict = Depends(verify_user)) -> dict:
    try:
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error verifying user: {str(e)}")