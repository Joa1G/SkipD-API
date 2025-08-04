from app.db.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Instituicao(Base):
    __tablename__ = "instituicoes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    limite_faltas: Mapped[float] = mapped_column(nullable=False, default=0.0)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    
    # Relacionamentos
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="instituicoes")
    materias: Mapped[list["Materia"]] = relationship("Materia", back_populates="instituicao", cascade="all, delete-orphan")

from app.models.usuario import Usuario
from app.models.materia import Materia