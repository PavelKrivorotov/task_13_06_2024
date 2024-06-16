import datetime
import uuid

from sqlalchemy import Result


def product_serializer(
    objs: Result[tuple[
        uuid.UUID,
        str,
        str,
        float,
        datetime.datetime,
        str, str
    ]]
) -> list[dict]:
    
    result: dict[uuid.UUID, dict] = {}
    for product_id, \
        product_title, \
        product_description, \
        product_price, \
        product_published, \
        category_key, \
        category_title, \
        category_description in objs.columns(
            'product_id',
            'product_title',
            'product_description',
            'product_price',
            'product_published',
            'category_key',
            'category_title',
            'category_description'
        ).all():

        product = result.get(product_id)

        if product is None:
            result.setdefault(
                product_id,
                {
                    'id': product_id,
                    'title': product_title,
                    'description': product_description,
                    'price': product_price,
                    'published': product_published,
                    'category': [
                        {
                            'key': category_key,
                            'title': category_title,
                            'description': category_description
                        }
                    ]
                }
            )

        else:
            product['category'].append(
                {
                    'key': category_key,
                    'title': category_title,
                    'description': category_description
                }
            )

    return list(result.values())

