import typing

import pytest
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from main.utils import get_url
from categories.models import Category

from products import urls
from products.models import Product, ProductCategory
from products.schemas import WriteProduct, UpdateProduct
from products.crud import product_crud, check_categories
from products.filters import ProductFilter

from tests.products.utils import (
    get_product_id_from_url,
    merge_products
)


@pytest.mark.asyncio(scope='function')
async def test_check_categories(
    db_session: AsyncSession,
    # raw_categories: list[dict[str, str]],
    create_categories: list[Category]
):
    
    state_1 = await check_categories(db_session, ['100'])
    assert state_1 == True

    state_2 = await check_categories(db_session, ['100', '300', '500'])
    assert state_2 == True

    state_3 = await check_categories(db_session, ['000'])
    assert state_3 == False


class TestProductCRUD:
    @pytest.mark.asyncio(scope='function')
    async def test_create_product(
        self,
        db_session: AsyncSession,
        create_categories: list[Category],
        raw_create_product__product_1: dict[str, typing.Any]
    ):
        
        categories = [c['key'] for c in raw_create_product__product_1['category']]
        data = WriteProduct(
            title=raw_create_product__product_1['title'],
            description=raw_create_product__product_1['description'],
            price=raw_create_product__product_1['price'],
            category=categories
        )

        product = await product_crud.create_product(db=db_session, data=data)
        product_url = product.get('product')
        assert isinstance(product_url, str)

        product_id = get_product_id_from_url(product_url)
        assert product_url == get_url(urls.Retrieve_Product.replace(':product-id', product_id))

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
        self,
        db_session: AsyncSession,
        create_product__product_1: Product,
        raw_update_product__product_1: dict[str, typing.Any]
    ):

        product_id = str(create_product__product_1.id)
        categories = [c['key'] for c in raw_update_product__product_1['category']]

        data = UpdateProduct(
            title=raw_update_product__product_1['title'],
            description=raw_update_product__product_1['description'],
            price=raw_update_product__product_1['price'],
            category=categories
        )

        product = await product_crud.update_product(
            db=db_session,
            product_id=product_id,
            data=data
        )
        product_url = product.get('product')
        assert isinstance(product_url, str)
        assert product_url == get_url(urls.Retrieve_Product.replace(':product-id', product_id))

        instance = await db_session.get(Product, product_id)
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
        self,
        db_session: AsyncSession,
        create_product__product_1: Product
    ):
        
        product_id = str(create_product__product_1.id)
        product = await product_crud.delete_product(db=db_session, product_id=product_id)
        assert product is None

        instance = await db_session.get(Product, product_id)
        # need refresh ?
        # await db_session.refresh(instance)
        assert instance is None

    @pytest.mark.asyncio(scope='function')
    async def test_retrieve_product(
        self,
        db_session: AsyncSession,
        raw_create_product__product_1: dict[str, typing.Any],
        create_product__product_1: Product
    ):

        product_id = str(create_product__product_1.id)
        product = await product_crud.retrieve_product(db_session, product_id=product_id)
        assert product == raw_create_product__product_1

        # clear db
        await db_session.execute(
            delete(Product)
            .where(Product.id == product_id)
        )
        await db_session.commit()

    @pytest.mark.asyncio(scope='function')
    async def test_list_products__none__filter(
        self,
        db_session: AsyncSession,
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
        
        filter = ProductFilter(
            category=None,
            min_price=0,
            max_price=999999,
            published='asc'
        )
        products = await product_crud.list_products(db=db_session, filter=filter)
        assert products == {
            'count': len(raw_products),
            'result': raw_products
        }

    @pytest.mark.asyncio(scope='function')
    async def test_list_products__published__filter(
        self,
        db_session: AsyncSession,
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

        filter = ProductFilter(
            category=None,
            min_price=0,
            max_price=999999,
            published='desc'
        )
        products = await product_crud.list_products(db=db_session, filter=filter)
        assert products == {
            'count': len(raw_products),
            'result': raw_products
        }

    @pytest.mark.asyncio(scope='function')
    async def test_list_products__category__filter(
        self,
        db_session: AsyncSession,
        create_products: list[tuple[Product, ProductCategory]],
        raw_product__seaweed: dict[str, typing.Any],
    ):
        
        raw_products = merge_products([raw_product__seaweed])

        filter = ProductFilter(
            category=['100', '500'],
            min_price=0,
            max_price=999999,
            published='asc'
        )
        products = await product_crud.list_products(db=db_session, filter=filter)
        assert products == {
            'count': len(raw_products),
            'result': raw_products
        }

    @pytest.mark.asyncio(scope='function')
    async def test_list_products__price__filter(
        self,
        db_session: AsyncSession,
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

        filter = ProductFilter(
            category=None,
            min_price=50,
            max_price=2000,
            published='asc'
        )
        products = await product_crud.list_products(db=db_session, filter=filter)
        assert products == {
            'count': len(raw_products),
            'result': raw_products
        }

    @pytest.mark.asyncio(scope='function')
    async def test_list_products__all__filter(
        self,
        db_session: AsyncSession,
        create_products: list[tuple[Product, ProductCategory]],
        raw_product__pineapple: dict[str, typing.Any],
    ):
        
        raw_products = merge_products([raw_product__pineapple], reverse=True)

        filter = ProductFilter(
            category=['400'],
            min_price=104.50,
            max_price=299,
            published='desc'
        )
        products = await product_crud.list_products(db=db_session, filter=filter)
        assert products == {
            'count': len(raw_products),
            'result': raw_products
        }

