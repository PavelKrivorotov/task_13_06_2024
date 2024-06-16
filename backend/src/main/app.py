from fastapi import FastAPI

from categories.routers import router as category_router
from products.routers import router as product_router


app = FastAPI()
app.include_router(category_router, prefix='/categories', tags=['Category'])
app.include_router(product_router, prefix='/products', tags=['Product'])

