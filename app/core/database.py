import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Detecta automaticamente se está no Render ou local
DATABASE_URL = os.getenv("DATABASE_URL")

# Se não tiver DATABASE_URL definida, usa SQLite local
if not DATABASE_URL:
    DATABASE_URL = "sqlite+aiosqlite:///./skipddb.db"
elif DATABASE_URL.startswith("postgres://"):
    # Render usa postgres://, mas SQLAlchemy precisa de postgresql://
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# Criar engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session maker
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency para FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()