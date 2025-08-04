from sqlalchemy.orm import Session
from app.models.materia import Materia
from app.schemas.materia import MateriaCreate, MateriaUpdate

def create_materia(db: Session, materia: MateriaCreate, instituicao_id: int):
    materia: Materia = Materia(**materia.model_dump(), instituicao_id=instituicao_id)
    db.add(materia)
    db.commit()
    db.refresh(materia)
    return materia

def get_materia(db: Session, materia_id: int):
    return db.query(Materia).filter(Materia.id == materia_id).first()

def get_materias_by_instituicao(db: Session, instituicao_id: int):
    return db.query(Materia).filter(Materia.instituicao_id == instituicao_id).all()

def update_materia(db: Session, materia_id: int, materia_data: MateriaUpdate):
    materia = get_materia(db, materia_id=materia_id)

    if materia:
        for field, value in materia_data.model_dump(exclude_unset=True).items():
            setattr(materia, field, value)
        db.commit()
        db.refresh(materia)
        return materia
    return None

def delete_materia(db: Session, materia_id: int):
    materia = get_materia(db, materia_id=materia_id)
    if materia:
        db.delete(materia)
        db.commit()
        return True
    return False