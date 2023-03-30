from typing import AsyncGenerator, Generator

from sqlalchemy.ext.asyncio import AsyncSession

from core.configs.database import async_session

# async def get_session() -> Generator:
#     session: AsyncSession = Session()

#     try:
#         yield session
#     finally:
#         await session.close()


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
