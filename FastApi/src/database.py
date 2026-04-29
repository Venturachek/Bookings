from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.config import settings
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(settings.db_url)
engine_null_pull = create_async_engine(settings.db_url, poolclass=NullPool)
async_session_maker_null_pull = async_sessionmaker(engine_null_pull, expire_on_commit=False)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


