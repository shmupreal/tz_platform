from fastapi import FastAPI
from .api.routes import product

app = FastAPI()

app.include_router(product.product_router)