from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.materia import *
from app.services.materia_service import *
from app.db.database import get_db, Session
from app.core.auth import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/subject", tags=["Matéria"])

@router.post("/{instituition_id}", response_model=MateriaRead, status_code=status.HTTP_201_CREATED)
def create_subject(instituition_id: int, materia: MateriaCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        if not decode_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return create_materia(db, materia, instituition_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/all/{instituition_id}", response_model=list[MateriaRead])
def get_subjects_by_instituition(instituition_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        if not decode_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return get_materias_by_instituicao(db, instituition_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/{materia_id}", response_model=MateriaRead)
def get_subject_by_id(materia_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        if not decode_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return get_materia(db, materia_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.put("/{materia_id}", response_model=MateriaRead)
def update_subject(materia_id: int, materia_data: MateriaUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        if not decode_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        updated_materia = update_materia(db, materia_id, materia_data)
        if not updated_materia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matéria not found")
        return updated_materia
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{materia_id}")
def delete_subject(materia_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        if not decode_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        if delete_materia(db, materia_id):
            return {"detail": "Matéria deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matéria not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))