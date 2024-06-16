import typing

from fastapi import Query
from sqlalchemy import TextClause

from main.validations import Published_Re_Validation
from products.models import Product, ProductCategory


class ProductFilter:
    def __init__(
        self,
        category: list[str] = Query(default=None),
        min_price: float = Query(default=0, ge=0, lt=1000000),
        max_price: float = Query(default=999999, ge=0, lt=1000000),
        published: str = Query(default='asc', pattern=Published_Re_Validation)
    ) -> None:
        
        self._errors = []

        self._category = category
        self._published = published

        if min_price > max_price:
            msg = 'Price error! min_price > max_price ({0} > {1})'.format(min_price, max_price)
            self._errors.append(msg)
        else:
            self._min_price = min_price
            self._max_price = max_price

    @property
    def errors(self) -> list[str]:
        return self._errors

    @property
    def category(self) -> typing.Optional[tuple[TextClause, dict]]:
        if self._category:
            category = []
            kwargs = {}
            for ind, cat in enumerate(self._category):
                s_value = 'category_{0}'.format(ind)
                s_cat = '{0}.category_key = :{1}'.format(
                    ProductCategory.__tablename__,
                    s_value
                )
                category.append(s_cat)
                kwargs.setdefault(s_value, cat)

            return (' OR '.join(category), kwargs)

    @property
    def category_count(self) -> int:
        return len(self._category)

    @property
    def price(self) -> typing.Optional[tuple[TextClause, dict]]:
        _where = '{0}.price BETWEEN :{1} AND :{2}'.format(
            Product.__tablename__,
            'min_price',
            'max_price'
        )
        kwargs = {
            'min_price': self._min_price,
            'max_price': self._max_price
        }
        return (_where, kwargs)

    @property
    def published(self) -> typing.Optional[str]:
        return self._published

