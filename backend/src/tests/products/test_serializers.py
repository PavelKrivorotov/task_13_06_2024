import typing

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from categories.models import Category

from products.models import Product, ProductCategory
from products.schemas import ListProduct
from products.queries import q_products
from products.serializers import product_serializer

from tests.products.utils import merge_products


@pytest.mark.asyncio
async def test_product_serializer(
    db_session: AsyncSession,
    create_products: list[tuple[Product, ProductCategory]],
    raw_product__apple: dict[str, typing.Any],
    raw_product__pineapple: dict[str, typing.Any],
    raw_product__potato: dict[str, typing.Any],
    raw_product__whiskey: dict[str, typing.Any],
    raw_product__seaweed: dict[str, typing.Any],
    raw_product__tuna: dict[str, typing.Any]
):
    
    s_query = (
        q_products()
        .order_by(
            Product.published,
            Category.key
        )
    )
    products = await db_session.execute(s_query)
    s_products = product_serializer(products)

    raw_products = merge_products([
        raw_product__apple,
        raw_product__pineapple,
        raw_product__potato,
        raw_product__whiskey,
        raw_product__seaweed,
        raw_product__tuna
    ])

    assert ListProduct(result=s_products).model_dump() == raw_products

