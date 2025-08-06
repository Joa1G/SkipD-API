from sqlalchemy.ext.declarative import declarative_base
from app.core.database import get_db, engine, AsyncSessionLocal

# Base para os models
Base = declarative_base()

# Re-exporta as funções e objetos necessários
__all__ = ["Base", "get_db", "engine", "AsyncSessionLocal"]