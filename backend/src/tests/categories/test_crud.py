import pytest
from sqlalchemy.ext.asyncio import AsyncSession

import products.models
from categories.models import Category
from categories.crud import category_crud


class TestCategoryCRUD:
    @pytest.mark.asyncio(scope='function')
    async def test_list_categories(
        self,
        db_session: AsyncSession,
        raw_categories: list[dict],
        create_categories: list[Category]
    ):
        
        result = await category_crud.list_categories(db_session)
        assert result == {
            'count': len(raw_categories),
            'result': raw_categories
        }

    @pytest.mark.asyncio(scope='function')
    async def test_list_categories_empty(
        self,
        db_session: AsyncSession
    ):
        
        result = await category_crud.list_categories(db_session)
        assert result == {
            'count': 0,
            'result': []
        }

