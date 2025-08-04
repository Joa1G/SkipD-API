from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/skipddb"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=30,
    pool_timeout=30,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)

class Base(DeclarativeBase):
    pass

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()