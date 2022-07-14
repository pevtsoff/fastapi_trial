import logging
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .settings import settings

logger = logging.getLogger(__name__)

# engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
# Session = sessionmaker(engine, autocommit=False, autoflush=True)


# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

logger.info("Connecting to database...")
engine = create_async_engine(
    settings.database_url,
    query_cache_size=0,
)

async def get_session() -> AsyncIterator[AsyncSession]:
    async_session = sessionmaker(autocommit=False, autoflush=True, bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


#two options to create a session
# async def get_session() -> AsyncIterator[AsyncSession]:
#     async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
#     try:
#         session = async_session()
#         yield session
#     except Exception as e:
#         logger.exception(e)
#         session.rollback()
#         raise





