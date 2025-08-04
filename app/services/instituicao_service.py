from sqlalchemy.orm import Session
from app.models.instituicao import Instituicao
from app.schemas.instituicao import InstituicaoCreate, InstituicaoUpdate

def create_instituicao(db: Session, instituicao: InstituicaoCreate, usuario_id: int):
    instituicao: Instituicao = Instituicao(**instituicao.model_dump(), id_usuario=usuario_id)
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