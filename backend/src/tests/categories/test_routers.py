import pytest
from httpx import AsyncClient

from categories import urls
from categories.models import Category


@pytest.mark.asyncio(scope='function')
async def test_list_categories(
    async_client: AsyncClient,
    raw_categories: list[dict],
    create_categories: list[Category]
):
    
    response = await async_client.get(url=urls.List_Categories)
    assert response.status_code == 200
    assert response.json() == {
        'count': len(raw_categories),
        'result': raw_categories
    }


@pytest.mark.asyncio(scope='function')
async def test_list_categories_empty(
    async_client: AsyncClient
):
    
    response = await async_client.get(url=urls.List_Categories)
    assert response.status_code == 200
    assert response.json() == {
        'count': 0,
        'result': []
    }

