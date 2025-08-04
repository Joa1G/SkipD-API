import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.routes import router
from app.api.instituicao_routes import router as instituicao_router
from app.api.usuario_routes import router as usuario_router
from app.api.materia_routes import router as materia_router
from app.db.database import Base, engine

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Criar as tabelas no banco de dados durante o startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup code can go here if needed

app = FastAPI(title="SkipD API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
app.include_router(instituicao_router, prefix="/api")
app.include_router(usuario_router, prefix="/api")
app.include_router(materia_router, prefix="/api")

