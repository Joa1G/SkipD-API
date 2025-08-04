from sqlalchemy.orm import Session
from app.models.instituicao import Instituicao
from app.schemas.instituicao import InstituicaoCreate, InstituicaoUpdate
from app.services.usuario_service import get_usuario
from fastapi import HTTPException

def create_instituicao(db: Session, instituicao: InstituicaoCreate, usuario_id: int):
    if not get_usuario(db, usuario_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    instituicao: Instituicao = Instituicao(**instituicao.model_dump(), usuario_id=usuario_id)
    db.add(instituicao)
    db.commit()
    db.refresh(instituicao)
    return instituicao

def get_instituicao(db: Session, instituicao_id: int):
    return db.query(Instituicao).filter(Instituicao.id == instituicao_id).first()

def get_instituicoes_by_usuario(db: Session, usuario_id: int):
    return db.query(Instituicao).filter(Instituicao.usuario_id == usuario_id).all()

def update_instituicao(db: Session, instituicao_id: int, instituicao_data: InstituicaoUpdate):
    instituicao = get_instituicao(db, instituicao_id=instituicao_id)

    if instituicao:
        for field, value in instituicao_data.model_dump(exclude_unset=True).items():
            setattr(instituicao, field, value)
        db.commit()
        db.refresh(instituicao)
        return instituicao
    return None

def delete_instituicao(db: Session, instituicao_id: int):
    instituicao = get_instituicao(db, instituicao_id=instituicao_id)
    if instituicao:
        db.delete(instituicao)
        db.commit()
        return True
    return False