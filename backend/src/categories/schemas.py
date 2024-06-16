import typing

from pydantic import BaseModel, ConfigDict
from pydantic import model_serializer


class ReadCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    title: str
    description: typing.Optional[str]


class ListCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: list[ReadCategory]

    @model_serializer
    def serializer(self) -> list[ReadCategory]:
        return self.result

