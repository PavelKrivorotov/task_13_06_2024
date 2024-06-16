import typing

import pytest
from httpx import AsyncClient
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from main.utils import get_url
from categories.models import Category

from products import urls
from products.models import Product, ProductCategory

from tests.products.utils import (
    get_product_id_from_url,
    merge_products
)


@pytest.mark.asyncio(scope='function')
async def test_create_product(
    db_session: AsyncSession,
    async_client: AsyncClient,
    create_categories: list[Category],
    raw_create_product__product_1: dict[str, typing.Any]
):
    
    categories = [c['key'] for c in raw_create_product__product_1['category']]
    response = await async_client.post(
        url=urls.Create_Product,
        data={
            'title': raw_create_product__product_1['title'],
            'description': raw_create_product__product_1['description'],
            'price': raw_create_product__product_1['price'],
            'category': categories
        }
    )
    assert response.status_code == 201

    product_url = response.json().get('product')
    assert isinstance(product_url, str)

    product_id = get_product_id_from_url(product_url)
    assert product_url == get_url(urls.Retrieve_Product.replace(':product-id', product_id))
    assert response.json() == {'product': product_url}

    instance = await db_session.get(Product, product_id)
    assert isinstance(instance, Product)
    assert instance.title == raw_create_product__product_1['title']
    assert instance.description == raw_create_product__product_1['description']
    assert float(instance.price) == raw_create_product__product_1['price']

    q_categories = (
        select(Category.key)
        .join_from(Category, ProductCategory, Category.key == ProductCategory.category_key)
        .where(ProductCategory.product_id == product_id)
    )
    _categories = await db_session.scalars(q_categories)
    assert sorted(categories) == sorted(list(_categories.all()))

    # clear db
    await db_session.execute(
        delete(Product)
        .where(Product.id == product_id)
    )
    await db_session.commit()


@pytest.mark.asyncio(scope='function')
async def test_update_product(
    db_session: AsyncSession,
    async_client: AsyncClient,
    create_product__product_1: Product,
    raw_update_product__product_1: dict[str, typing.Any]
):
    
    categories = [c['key'] for c in raw_update_product__product_1['category']]
    url = urls.Update_Product.replace(':product-id', str(create_product__product_1.id))
    response = await async_client.patch(
        url=url,
        data={
            'title': raw_update_product__product_1['title'],
            'description': raw_update_product__product_1['description'],
            'price': raw_update_product__product_1['price'],
            'category': categories
        }
    )
    assert response.status_code == 202

    product_url = response.json().get('product')
    assert isinstance(product_url, str)

    product_id = get_product_id_from_url(product_url)
    assert product_url == get_url(urls.Retrieve_Product.replace(':product-id', product_id))
    assert response.json() == {'product': product_url}

    instance = await db_session.get(Product, product_id)
    # lol need refresh, because data receive BEFORE update!
    await db_session.refresh(instance)

    assert isinstance(instance, Product)
    assert instance.title == raw_update_product__product_1['title']
    assert instance.description == raw_update_product__product_1['description']
    assert float(instance.price) == raw_update_product__product_1['price']

    q_categories = (
        select(Category.key)
        .join_from(Category, ProductCategory, Category.key == ProductCategory.category_key)
        .where(ProductCategory.product_id == product_id)
    )
    _categories = await db_session.scalars(q_categories)
    assert sorted(categories) == sorted(list(_categories.all()))

    # clear db
    await db_session.execute(
        delete(Product)
        .where(Product.id == product_id)
    )
    await db_session.commit()


@pytest.mark.asyncio(scope='function')
async def test_delete_product(
    db_session: AsyncSession,
    async_client: AsyncClient,
    create_product__product_1: Product
):
    
    product_id = str(create_product__product_1.id)
    url = urls.Delete_Product.replace(':product-id', product_id)
    response = await async_client.delete(url=url)
    assert response.status_code == 204

    instance = await db_session.get(Product, product_id)
    # need refresh ?
    # await db_session.refresh(instance)

    assert instance is None


@pytest.mark.asyncio(scope='function')
async def test_retrieve_product(
    db_session: AsyncSession,
    async_client: AsyncClient,
    raw_create_product__product_1: dict[str, typing.Any],
    create_product__product_1: Product
):
    
    product_id = str(create_product__product_1.id)
    url = urls.Retrieve_Product.replace(':product-id', product_id)
    response = await async_client.get(url=url)
    assert response.status_code == 200
    assert response.json() == raw_create_product__product_1

    # clear db
    await db_session.execute(
        delete(Product)
        .where(Product.id == product_id)
    )
    await db_session.commit()


@pytest.mark.asyncio(scope='function')
async def test_list_products__none__filter(
    async_client: AsyncClient,
    create_products: list[tuple[Product, ProductCategory]],
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
    
    response = await async_client.get(url=urls.List_Products)
    assert response.status_code == 200
    assert response.json() == {
        'count': len(raw_products),
        'result': raw_products
    }

@pytest.mark.asyncio(scope='function')
async def test_list_products__published__filter(
    async_client: AsyncClient,
    create_products: list[tuple[Product, ProductCategory]],
    raw_product__apple: dict[str, typing.Any],
    raw_product__pineapple: dict[str, typing.Any],
    raw_product__potato: dict[str, typing.Any],
    raw_product__whiskey: dict[str, typing.Any],
    raw_product__seaweed: dict[str, typing.Any],
    raw_product__tuna: dict[str, typing.Any]
):
    
    raw_products = merge_products(
        [
            raw_product__apple,
            raw_product__pineapple,
            raw_product__potato,
            raw_product__whiskey,
            raw_product__seaweed,
            raw_product__tuna
        ],
        reverse=True
    )

    response = await async_client.get(
        url=urls.List_Products,
        params={
            'published': 'desc'
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'count': len(raw_products),
        'result': raw_products
    }

@pytest.mark.asyncio(scope='function')
async def test_list_products__category__filter(
    async_client: AsyncClient,
    create_products: list[tuple[Product, ProductCategory]],
    raw_product__seaweed: dict[str, typing.Any],
):
    
    raw_products = merge_products([raw_product__seaweed])

    response = await async_client.get(
        url=urls.List_Products,
        params={
            'category': ['100', '500']
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'count': len(raw_products),
        'result': raw_products
    }

@pytest.mark.asyncio(scope='function')
async def test_list_products__price__filter(
    async_client: AsyncClient,
    create_products: list[tuple[Product, ProductCategory]],
    raw_product__apple: dict[str, typing.Any],
    raw_product__pineapple: dict[str, typing.Any],
    raw_product__whiskey: dict[str, typing.Any],
    raw_product__seaweed: dict[str, typing.Any],
):
    
    raw_products = merge_products([
        raw_product__apple,
        raw_product__pineapple,
        raw_product__whiskey,
        raw_product__seaweed
    ])

    response = await async_client.get(
        url=urls.List_Products,
        params={
            'min_price': 50,
            'max_price': 2000
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'count': len(raw_products),
        'result': raw_products
    }

@pytest.mark.asyncio(scope='function')
async def test_list_products__all__filter(
    async_client: AsyncClient,
    create_products: list[tuple[Product, ProductCategory]],
    raw_product__pineapple: dict[str, typing.Any],
):
    
    raw_products = merge_products([raw_product__pineapple], reverse=True)

    response = await async_client.get(
        url=urls.List_Products,
        params={
            'category': ['400'],
            'min_price': 104.50,
            'max_price': 299,
            'published': 'desc'
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'count': len(raw_products),
        'result': raw_products
    }

