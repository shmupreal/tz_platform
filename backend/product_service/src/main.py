from fastapi import FastAPI
from .api.routes import product
from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from redis import asyncio as aioredis

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        redis = aioredis.from_url("redis://redis_app:6379/0")
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        yield
    except aioredis.RedisError as e:
        raise HTTPException(status_code=502, detail=f"Error connecting to Redis: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {e}")

app = FastAPI(lifespan=lifespan)

app.include_router(product.product_router)