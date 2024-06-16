from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from main import settings


url = URL.create(
    drivername=settings.DATABASE['DRIVER'],
    username=settings.DATABASE['USER'],
    password=settings.DATABASE['PASSWORD'],
    database=settings.DATABASE['NAME'],
    host=settings.DATABASE['HOST'],
    port=settings.DATABASE['PORT']
)

engine = create_async_engine(url=url)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass

