from typing import TYPE_CHECKING
from app.db.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.instituicao import Instituicao

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(nullable=False)
    is_premium: Mapped[bool] = mapped_column(default=False)
    url_foto: Mapped[str] = mapped_column(default="")
    
    # Relacionamento com Instituicao
    instituicoes: Mapped[list["Instituicao"]] = relationship("Instituicao", back_populates="usuario", cascade="all, delete-orphan")