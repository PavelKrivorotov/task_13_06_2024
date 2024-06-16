import datetime
import uuid

from sqlalchemy import Uuid, Integer, String, Text, Numeric, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from main.db import Base
from categories.models import Category


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text
    )
    price: Mapped[float] = mapped_column(
        Numeric(8, 2),
        nullable=False
    )
    published: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        index=True,
        server_default=func.now(),
        nullable=False
    )

    category = relationship('ProductCategory')


class ProductCategory(Base):
    __tablename__ = 'product_category'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Product.id, ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    category_key: Mapped[str] = mapped_column(
        ForeignKey(Category.key, ondelete='CASCADE'),
        index=True,
        nullable=False
    )

