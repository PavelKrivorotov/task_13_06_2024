import typing

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from categories.models import Category
from products.models import Product, ProductCategory

from tests.products.utils import (
    merge_products,
    make_product_and_p_category_from_raw
)


# create
@pytest_asyncio.fixture(scope='function')
async def raw_create_product__product_1():
    product = {
        'id': '6e5f886e-1292-4a8f-9dd4-3cf7bbd6d2c0',
        'title': 'Product-1',
        'description': None,
        'price': 987.72,
        'published': '2024-06-15 18:00:01',
        'category': [
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
                'key': '400',
                'title': 'Fruits',
                'description': 'About Fruits'
            }
        ]
    }
    yield product

@pytest_asyncio.fixture(scope='function')
async def create_product__product_1(
    db_session: AsyncSession,
    create_categories: list[Category],
    raw_create_product__product_1: dict[str, typing.Any]
):
    
    product, p_categories = make_product_and_p_category_from_raw(raw_create_product__product_1)
    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)

    db_session.add_all(p_categories)
    await db_session.commit()

    yield product


# update
@pytest_asyncio.fixture(scope='function')
async def raw_update_product__product_1(
    raw_create_product__product_1: dict[str, typing.Any]
):
    
    product = raw_create_product__product_1
    product['title'] = 'Product-1-UPDATE'
    product['description'] = '...about Product-1-UPDATE'
    product['price'] = 123456.78
    product['category'] = [
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
    yield product


# list
@pytest_asyncio.fixture(scope='function')
async def raw_product__apple():
    product =  {
        'id': 'd14e05e2-3c87-403f-8cd6-4bd248d784f1',
        'title': 'Apple',
        'description': '...about Apple',
        'price': 104.49,
        'published': '2024-06-15 18:00:01',
        'category': [
            {
                'key': '400',
                'title': 'Fruits',
                'description': 'About Fruits'
            }
        ]
    }
    yield product

@pytest_asyncio.fixture(scope='function')
async def raw_product__pineapple():
    product = {
        'id': '28f2f21c-d448-49b7-8c44-5e29b3733f30',
        'title': 'Pineapple',
        'description': None,
        'price': 289.90,
        'published': '2024-06-15 18:00:00',
        'category': [
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
    }
    yield product

@pytest_asyncio.fixture(scope='function')
async def raw_product__potato():
    product = {
        'id': 'd0eaf939-4531-4d5e-a502-d9ab1f082ae6',
        'title': 'Potato',
        'description': None,
        'price': 49.99,
        'published': '2024-06-15 12:59:59',
        'category': [
            {
                'key': '500',
                'title': 'Vegetables',
                'description': 'About Vegetables'
            }
        ]
    }
    yield product

@pytest_asyncio.fixture(scope='function')
async def raw_product__whiskey():
    product = {
        'id': 'd6ea13c5-d2db-49c0-87c5-b407f47a0f82',
        'title': 'Whiskey',
        'description': '...about Whiskey',
        'price': 1999.00,
        'published': '2024-06-14 13:00:00',
        'category': [
            {
                'key': '200',
                'title': 'Alcohol',
                'description': 'About Alcohol'
            },
        ]
    }
    yield product

@pytest_asyncio.fixture(scope='function')
async def raw_product__seaweed():
    product = {
        'id': '13f891a7-d7df-4ca6-81b4-7ee1a8da22e6',
        'title': 'Seaweed',
        'description': '... about Seaweed',
        'price': 421.23,
        'published': '2024-06-16 21:02:41',
        'category': [
            {
                'key': '100',
                'title': 'Fish',
                'description': 'About Fish'
            },
            {
                'key': '500',
                'title': 'Vegetables',
                'description': 'About Vegetables'
            }
        ]
    }
    yield product

@pytest_asyncio.fixture(scope='function')
async def raw_product__tuna():
    product = {
        'id': 'abe389fb-1f68-40da-98b5-c3f831620e16',
        'title': 'Tuna',
        'description': '...abiut Tuna',
        'price': 499000.00,
        'published': '2024-06-16 22:00:00',
        'category': [
            {
                'key': '100',
                'title': 'Fish',
                'description': 'About Fish'
            }
        ]
    }
    yield product

@pytest_asyncio.fixture(scope='function')
async def create_products(
    db_session: AsyncSession,
    create_categories: list[Category],
    raw_product__apple: dict[str, typing.Any],
    raw_product__pineapple: dict[str, typing.Any],
    raw_product__potato: dict[str, typing.Any],
    raw_product__whiskey: dict[str, typing.Any],
    raw_product__seaweed: dict[str, typing.Any],
    raw_product__tuna: dict[str, typing.Any]
):

    raw_products = merge_products([
        raw_product__apple,
        raw_product__pineapple,
        raw_product__potato,
        raw_product__whiskey,
        raw_product__seaweed,
        raw_product__tuna
    ])
    
    products: list[Product] = []
    p_categories: list[ProductCategory] = []

    for raw in raw_products:
        product, p_category = make_product_and_p_category_from_raw(raw)
        products.append(product)
        p_categories.extend(p_category)

    db_session.add_all(products)
    await db_session.commit()

    db_session.add_all(p_categories)
    await db_session.commit()

    yield list(zip(products, p_categories))

    for p_category in p_categories:
        await db_session.delete(p_category)

    for product in products:
        await db_session.delete(product)

    await db_session.commit()

