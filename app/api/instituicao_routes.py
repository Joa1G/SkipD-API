from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.instituicao import *
from app.services.instituicao_service import *
from app.db.database import get_db, Session
from app.core.auth import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/instituition", tags=["Instituição"])

@router.post("/{user_id}", response_model=InstituicaoRead, status_code=status.HTTP_201_CREATED)
def create_instituition(user_id: int, instituicao: InstituicaoCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        if not decode_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return create_instituicao(db, instituicao, user_id)
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/all/{user_id}", response_model=list[InstituicaoRead])
def get_instituitions_by_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        if not decode_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return get_instituicoes_by_usuario(db, user_id)
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{instituicao_id}", response_model=InstituicaoRead)
def get_instituition_by_id(instituicao_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        if not decode_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return get_instituicao(db, instituicao_id)
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{instituicao_id}", response_model=InstituicaoRead)
def update_instituition(instituicao_id: int, instituicao_data: InstituicaoUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        if not decode_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        updated_instituicao = update_instituicao(db, instituicao_id, instituicao_data)
        if not updated_instituicao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituição not found")
        return updated_instituicao
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{instituicao_id}")
def delete_instituition(instituicao_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        if not decode_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        deleted = delete_instituicao(db, instituicao_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituição not found")
        return {"detail": "Instituição deleted successfully"}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

