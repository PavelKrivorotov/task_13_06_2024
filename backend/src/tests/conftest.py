import typing

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from main.utils import get_backend_url
from categories.models import Category

from tests.db import async_session


@pytest_asyncio.fixture(scope='function')
async def db_session() -> typing.AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

@pytest.fixture(scope='function')
def override_get_async_session(db_session: AsyncSession) -> typing.Callable:
    async def _override_get_async_session():
        yield db_session

    return _override_get_async_session

@pytest.fixture(scope='function')
def app(override_get_async_session) -> FastAPI:
    from main.db import get_db
    from main.app import app

    app.dependency_overrides[get_db] = override_get_async_session
    return app

@pytest_asyncio.fixture(scope='function')
async def async_client(app: FastAPI) -> typing.AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=get_backend_url()) as client:
        yield client


# 
@pytest_asyncio.fixture(scope='function')
async def raw_categories():
    categories = [
        {
            'key': '100',
            'title': 'Fish',
            'description': 'About Fish'
        },
        {
            'key': '200',
            'title': 'Alcohol',
            'description': 'About Alcohol'
        },
        {
            'key': '300',
            'title': 'Meat',
            'description': 'About Meat'
        },
        {
            'key': '400',
            'title': 'Fruits',
            'description': 'About Fruits'
        },
        {
            'key': '500',
            'title': 'Vegetables',
            'description': 'About Vegetables'
        }
    ]
    yield categories

@pytest_asyncio.fixture(scope='function')
async def create_categories(
    db_session: AsyncSession,
    raw_categories: list[dict]
):
    objs = []
    for raw in raw_categories:
        obj = Category(**raw)
        db_session.add(obj)
        objs.append(obj)

    await db_session.commit()
    yield objs

    for obj in objs:
        await db_session.delete(obj)
        await db_session.commit()

    await db_session.commit()

