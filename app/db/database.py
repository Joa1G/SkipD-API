from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/skipddb"

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with SessionLocal() as session:
        yield session