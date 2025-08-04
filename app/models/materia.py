from app.db.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Materia(Base):
    __tablename__ = "materias"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    carga_horaria: Mapped[int] = mapped_column(nullable=False, default=0)
    faltas: Mapped[int] = mapped_column(nullable=False, default=0)
    status: Mapped[str] = mapped_column(nullable=False)
    aulas_domingo: Mapped[int] = mapped_column(nullable=False, default=0)
    aulas_segunda: Mapped[int] = mapped_column(nullable=False, default=0)
    aulas_terca: Mapped[int] = mapped_column(nullable=False, default=0)
    aulas_quarta: Mapped[int] = mapped_column(nullable=False, default=0)
    aulas_quinta: Mapped[int] = mapped_column(nullable=False, default=0)
    aulas_sexta: Mapped[int] = mapped_column(nullable=False, default=0)
    aulas_sabado: Mapped[int] = mapped_column(nullable=False, default=0)
    instituicao_id: Mapped[int] = mapped_column(ForeignKey("instituicoes.id"), nullable=False)
    
    # Relacionamento com Instituicao
    instituicao: Mapped["Instituicao"] = relationship("Instituicao", back_populates="materias")

from app.models.instituicao import Instituicao