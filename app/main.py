from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.instituicao_routes import router as instituicao_router
from app.api.usuario_routes import router as usuario_router
from app.api.materia_routes import router as materia_router
from app.db.database import Base, engine

app = FastAPI(title="SkipD API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")
app.include_router(instituicao_router, prefix="/api")
app.include_router(usuario_router, prefix="/api")
app.include_router(materia_router, prefix="/api")

