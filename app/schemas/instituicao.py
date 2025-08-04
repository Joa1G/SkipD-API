from pydantic import BaseModel
from typing import Optional

class Instituicao(BaseModel):
    nome: str
    limite_faltas: float
    usuario_id: int

class InstituicaoCreate(Instituicao):
    pass

class InstituicaoRead(Instituicao):
    id: int
    class Config:
        from_attributes = True

class InstituicaoUpdate(BaseModel):
    nome: Optional[str] = None
    limite_faltas: Optional[float] = None
    usuario_id: Optional[int] = None