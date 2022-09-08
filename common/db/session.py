from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from common import config

# local hardcode
# SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://postgres:1@localhost:5432/fastapi_scg"

DATABASE_HOSTNAME = config.DATABASE_HOSTNAME
DATABASE_PORT = config.DATABASE_PORT
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_NAME = config.DATABASE_NAME
DATABASE_USERNAME = config.DATABASE_USERNAME

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{DATABASE_NAME}"

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"


Base = declarative_base()


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()