from pydantic import BaseModel
from typing import Optional

class Materia(BaseModel):
    nome: str
    carga_horaria: int
    faltas: int
    status: str
    aulas_domingo: int
    aulas_segunda: int
    aulas_terca: int
    aulas_quarta: int
    aulas_quinta: int
    aulas_sexta: int
    aulas_sabado: int
    instituicao_id: int

class MateriaCreate(Materia):
    pass

class MateriaRead(Materia):
    id: int
    class Config:
        from_attributes = True

class MateriaUpdate(BaseModel):
    nome: Optional[str] = None
    carga_horaria: Optional[int] = None
    faltas: Optional[int] = None
    status: Optional[str] = None
    aulas_domingo: Optional[int] = None
    aulas_segunda: Optional[int] = None
    aulas_terca: Optional[int] = None
    aulas_quarta: Optional[int] = None
    aulas_quinta: Optional[int] = None
    aulas_sexta: Optional[int] = None
    aulas_sabado: Optional[int] = None
    instituicao_id: Optional[int] = None