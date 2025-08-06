import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Detecta automaticamente se está no Render ou local
DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Original DATABASE_URL: {DATABASE_URL}")

# Se não tiver DATABASE_URL definida, usa SQLite local
if not DATABASE_URL:
    DATABASE_URL = "sqlite+aiosqlite:///./skipddb.db"
    print("Using SQLite database for local development")
else:
    # Forçar uso do asyncpg para PostgreSQL
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
        print("Converted postgres:// to postgresql+asyncpg://")
    elif DATABASE_URL.startswith("postgresql://") and "+asyncpg" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        print("Added asyncpg driver to postgresql://")
    
    print("Using PostgreSQL database for production")

print(f"Final DATABASE_URL: {DATABASE_URL[:50]}...")

# Configurações mais simples para evitar problemas
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs = {"echo": False}
else:
    engine_kwargs = {"echo": False, "pool_pre_ping": True}

# Criar engine
engine = create_async_engine(DATABASE_URL, **engine_kwargs)
print("Database engine created successfully")

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