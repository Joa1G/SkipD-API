from pydantic import BaseModel
from typing import Optional

class Instituicao(BaseModel):
    nome: str
    limite_faltas: float

class InstituicaoCreate(Instituicao):
    pass

class InstituicaoRead(Instituicao):
    usuario_id: int
    id: int
    class Config:
        from_attributes = True

class InstituicaoUpdate(BaseModel):
    nome: Optional[str] = None
    limite_faltas: Optional[float] = None