from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from main.db import Base
from categories.utils import gen_category_key


class Category(Base):
    __tablename__ = 'categories'

    key: Mapped[str] = mapped_column(
        String(8),
        primary_key=True,
        default=gen_category_key
    )
    title: Mapped[str] = mapped_column(
        String(255),
        index=True,
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text
    )

    product = relationship('ProductCategory')

