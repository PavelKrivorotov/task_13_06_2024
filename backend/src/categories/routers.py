from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from main.db import get_db


router = APIRouter()


from categories.crud import category_crud

@router.get('/')
async def list_categories(
    db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    
    categories = await category_crud.list_categories(db)
    return JSONResponse(content=categories)

