import typing
import datetime
import uuid

from fastapi import Form

from pydantic import BaseModel, ConfigDict
from pydantic import model_serializer, field_serializer

from main.utils import get_url
from categories.schemas import ReadCategory
from products.urls import Retrieve_Product


class BaseProduct:
    def _clean_category(self, values: list[str]) -> list[str]:
        if len(values) == 1:
            # if category[0]: ?
            categories = values[0].split(',')
        else:
            categories = [category for category in values if category]

        return sorted(list(set(categories)))


class WriteProduct(BaseProduct):
    def __init__(
        self,
        title: str = Form(
            min_length=1,
            max_length=255
        ),
        description: str = Form(
            default=None
        ),
        price: float = Form(
            gt=0,
            lt=1000000
        ),
        category: list[str] = Form(
            min_length=1
        )
    ) -> None:
        
        self.title = title
        self.description = description
        self.price = price
        self.category = self._clean_category(category)

    @property
    def dict(self) -> dict[str, typing.Any]:
        _dict = {}
        for attr in self.__dict__:
            value = self.__getattribute__(attr)
            _dict.setdefault(attr, value)

        return _dict


class UpdateProduct(BaseProduct):
    def __init__(
        self,
        title: str = Form(
            min_length=1,
            max_length=255,
            default=None
        ),
        description: str = Form(
            default=None
        ),
        price: float = Form(
            gt=0,
            lt=1000000,
            default=None
        ),
        category: list[str] = Form(
            default=None
        )
    ) -> None:
        
        self.title = title
        self.description = description
        self.price = price
        self.category = self._clean_category(category)
    
    @property
    def dict(self) -> dict[str, typing.Any]:
        _dict = {}
        for attr in self.__dict__:
            value = self.__getattribute__(attr)

            if value:
                _dict.setdefault(attr, value)

        return _dict


class ReadProductShort(BaseModel):
    product_id: uuid.UUID

    @model_serializer
    def serializer(self) -> dict[str, str]:
        path = Retrieve_Product.replace(':product-id', str(self.product_id))
        url = get_url(path)
        return {'product': url}


class ReadProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: typing.Optional[str]
    price: float
    published: datetime.datetime

    category: list[ReadCategory]

    @field_serializer('id')
    def serialize_id(id: uuid.UUID) -> str:
        return str(id)

    @field_serializer('published')
    def serializer_published(published: datetime.datetime) -> str:
        return published.strftime('%Y-%m-%d %H:%M:%S')


class ListProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: list[ReadProduct]

    @model_serializer
    def serializer(self) -> list[ReadProduct]:
        return self.result

