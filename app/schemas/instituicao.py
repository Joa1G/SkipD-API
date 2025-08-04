from pydantic import BaseModel
from typing import Optional

class Instituicao(BaseModel):
    nome: str
    limite_faltas: float
    id_usuario: int

class InstituicaoCreate(Instituicao):
    pass

class InstituicaoRead(Instituicao):
    id: int
    class Config:
        from_attributes = True

class InstituicaoUpdate(BaseModel):
    nome: Optional[str] = None
    limite_faltas: Optional[float] = None
    id_usuario: Optional[int] = None