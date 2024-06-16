import re
import typing
import datetime
import uuid

from main.validations import UUID_Re_Validation
from products.models import Product, ProductCategory


def get_product_id_from_url(url: str) -> typing.Optional[str]:
    pattern = UUID_Re_Validation[1:len(UUID_Re_Validation) - 1]
    product_id = re.search(pattern, url)

    if product_id:
        return product_id[0]

def merge_products(
    values: list[dict[str, typing.Any]],
    reverse: bool = False,
) -> list[dict[str, typing.Any]]:
    
    products = []
    for value in values:
        value['category'].sort(key=lambda value: value['key'])
        products.append(value)

    products.sort(
        key=lambda value: datetime.datetime.fromisoformat(value['published']),
        reverse=reverse
    )
    return products

def make_product_and_p_category_from_raw(
    raw: dict[str, typing.Any]
) -> tuple[Product, list[ProductCategory]]:
    
    product = Product(
        id=uuid.UUID(raw['id']),
        title=raw['title'],
        description=raw['description'],
        price=raw['price'],
        published=datetime.datetime.fromisoformat(raw['published'])
    )

    categories = raw['category']
    p_categories: list[ProductCategory] = []
    for category in categories:
        p_category = ProductCategory(
            product_id=uuid.UUID(raw['id']),
            category_key=category['key']
        )
        p_categories.append(p_category)

    return (product, p_categories)

