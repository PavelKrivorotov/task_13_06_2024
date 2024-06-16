from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.responses import Response, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from main.db import get_db
from products.depends import get_product_or_error
from products.schemas import WriteProduct, UpdateProduct
from products.crud import product_crud, check_categories
from products.filters import ProductFilter


router = APIRouter()


@router.get('/')
async def list_products(
    filter: ProductFilter = Depends(),
    db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    
    if filter.errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='\n'.join(filter.errors)
        )
    
    products = await product_crud.list_products(db, filter)
    return JSONResponse(content=products)


@router.get('/{product_id}')
async def retrieve_product(
    product_id: str = Depends(get_product_or_error),
    db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    
    product = await product_crud.retrieve_product(db, product_id)
    return JSONResponse(content=product)


@router.post('/new')
async def create_product(
    data: WriteProduct = Depends(),
    db: AsyncSession = Depends(get_db)
) -> JSONResponse:

    if not (await check_categories(db, data.category)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid category key(s): ({})!'.format(', '.join(data.category))
        )
    
    product = await product_crud.create_product(db, data)
    return JSONResponse(
        content=product,
        status_code=status.HTTP_201_CREATED
    )


@router.patch('/update/{product_id}')
async def update_product(
    product_id: str = Depends(get_product_or_error),
    data: UpdateProduct = Depends(),
    db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    
    if not (await check_categories(db, data.category)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid category key(s): ({})!'.format(', '.join(data.category))
        )
    
    product = await product_crud.update_product(db, product_id, data)
    return JSONResponse(
        content=product,
        status_code=status.HTTP_202_ACCEPTED
    )


@router.delete('/delete/{product_id}')
async def delete_product(
    product_id: str = Depends(get_product_or_error),
    db: AsyncSession = Depends(get_db)
) -> Response:
    
    await product_crud.delete_product(db, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

