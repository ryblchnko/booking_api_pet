from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import DATABASE_URL, TEST_DATABASE_URL, settings

if settings.MODE == 'TEST':
    DATABASE_URL = TEST_DATABASE_URL
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


