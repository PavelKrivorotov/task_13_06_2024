import typing

from sqlalchemy import select
from sqlalchemy import Select

from categories.models import Category
from products.models import Product, ProductCategory


def q_products() -> Select[typing.Any]:
    query = (
        select(
            Product.id.label('product_id'),
            Product.title.label('product_title'),
            Product.description.label('product_description'),
            Product.price.label('product_price'),
            Product.published.label('product_published'),
            Category.key.label('category_key'),
            Category.title.label('category_title'),
            Category.description.label('category_description')
        )
        .join_from(Product, ProductCategory, Product.id == ProductCategory.product_id, isouter=True)
        .join_from(ProductCategory, Category, ProductCategory.category_key == Category.key, isouter=True)
    )

    return query

