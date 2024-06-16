import typing
import uuid

from sqlalchemy import func, text
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from categories.models import Category
from products.models import Product, ProductCategory
from products.schemas import (
    WriteProduct,
    UpdateProduct,
    ReadProductShort,
    ReadProduct,
    ListProduct
)
from products.filters import ProductFilter
from products.queries import q_products
from products.serializers import product_serializer


async def check_categories(
    db: AsyncSession,
    categories: list[str]
) -> bool:
    
    query = select(
        select(1)
        .where(
            text("string_to_array(:values, ',')::VARCHAR[] <@ (SELECT array_agg(key) FROM categories)")
        )
        .exists()
    )
    state = await db.scalar(query, {'values': ','.join(categories)})
    return state


class ProductCRUD:
    async def create_product(
        self,
        db: AsyncSession,
        data: WriteProduct
    ) -> dict[str, typing.Any]:
        
        product_id = uuid.uuid4()
        
        ddata = data.dict
        ddata.setdefault('id', product_id)
        categories = ddata.pop('category')

        product = Product(**ddata)
        db.add(product)

        for category in categories:
            p_category = ProductCategory(product_id=product_id, category_key=category)
            db.add(p_category)

        await db.commit()        
        return ReadProductShort(product_id=product_id).model_dump()

    async def update_product(
        self,
        db: AsyncSession,
        product_id: str,
        data: UpdateProduct
    ) -> dict[str, typing.Any]:
        
        ddata = data.dict
        categories = ddata.pop('category', [])

        if ddata:
            u_query = update(Product).where(Product.id == product_id).values(ddata)
            await db.execute(u_query)

        if categories:
            s_query = select(ProductCategory).where(ProductCategory.product_id == product_id)
            p_categories = await db.scalars(s_query)

            e_categories = []
            for category in p_categories.all():
                if category.category_key in categories:
                    e_categories.append(category.category_key)
                else:
                    await db.delete(category)

            for category in list(set(categories) - set(e_categories)):
                p_category = ProductCategory(product_id=product_id, category_key=category)
                db.add(p_category)

        await db.commit()
        return ReadProductShort(product_id=product_id).model_dump()

    async def delete_product(
        self,
        db: AsyncSession,
        product_id: str,
    ) -> None:
        
        query = delete(Product).where(Product.id == product_id)
        await db.execute(query)
        await db.commit()

    async def retrieve_product(
        self,
        db: AsyncSession,
        product_id: str
    ) -> dict[str, typing.Any]:

        p_query = (
            q_products()
            .where(Product.id == product_id)
            .order_by(Category.key)
        )
        product = await db.execute(p_query)

        s_product = product_serializer(product)
        return ReadProduct.model_validate(s_product[0]).model_dump()

    async def list_products(
        self,
        db: AsyncSession,
        filter: ProductFilter
    ) -> dict[str, typing.Any]:

        s_products_subquery = (
            select(ProductCategory.product_id)
            .join_from(Product, ProductCategory, Product.id == ProductCategory.product_id, isouter=True)
        )
        kwargs = {}

        # add category filter
        if filter.category is not None:
            s_products_subquery = (
                s_products_subquery
                .where(
                    text(filter.category[0])
                )
                .group_by(ProductCategory.product_id)
                .having(func.count(ProductCategory.product_id) == filter.category_count)
            )
            kwargs = kwargs | filter.category[1]

        # add price filter
        if filter.price is not None:
            s_products_subquery = s_products_subquery.where(
                text(filter.price[0])
            )
            kwargs = kwargs | filter.price[1]

        # c_query = (
        #     select(func.count())
        #     .select_from(
        #      s_products_subquery
        #      .distinct())
        # )
        c_query = (
            select(func.count())
            .select_from(
                s_products_subquery
                .distinct()
                .subquery()
            )
        )
        count = await db.scalar(c_query, kwargs)

        s_query = q_products()
        s_query = s_query.where(Product.id.in_(s_products_subquery))

        # add published filter
        if filter.published == 'asc':
            s_query = s_query.order_by(Product.published.asc(), Category.key)

        elif filter.published == 'desc':
            s_query = s_query.order_by(Product.published.desc(), Category.key)

        products = await db.execute(s_query, kwargs)

        s_products = product_serializer(products)
        l_products = ListProduct(result=s_products).model_dump()
        return {'count': count, 'result': l_products}

product_crud = ProductCRUD()

