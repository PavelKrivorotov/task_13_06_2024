from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from sqlalchemy.pool import NullPool

from main import settings


url = URL.create(
    drivername=settings.TEST_DATABASE['DRIVER'],
    username=settings.TEST_DATABASE['USER'],
    password=settings.TEST_DATABASE['PASSWORD'],
    database=settings.TEST_DATABASE['NAME'],
    host=settings.TEST_DATABASE['HOST'],
    port=settings.TEST_DATABASE['PORT']
)

# engine = create_async_engine(url=url) -> RuntimeError!

engine = create_async_engine(url=url, poolclass=NullPool)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

