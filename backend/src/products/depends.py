from fastapi import Depends, Path
from fastapi import status, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from main.db import get_db
from main.validations import UUID_Re_Validation
from products.models import Product


async def get_product_or_error(
    product_id: str = Path(pattern=UUID_Re_Validation),
    db: AsyncSession = Depends(get_db)
) -> str:
    
    query = select(
        select(Product)
        .where(Product.id == product_id)
        .exists()
    )
    state = await db.scalar(query)

    if state:
        return product_id
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='The product ({}) is not exists!'.format(product_id)
    )

