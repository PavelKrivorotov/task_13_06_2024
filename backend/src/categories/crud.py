import typing

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from categories.models import Category
from categories.schemas import ListCategory


class CategoryCRUD:
    async def list_categories(self, db: AsyncSession) -> dict[str, typing.Any]:
        c_query = select(func.count(Category.key))
        count = await db.scalar(c_query)

        s_query = (
            select(Category)
            .order_by(Category.key)
        )
        categories = await db.scalars(s_query)

        l_categories = ListCategory(result=categories.all()).model_dump()
        return {'count': count, 'result': l_categories}

category_crud = CategoryCRUD()

