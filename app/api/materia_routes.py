from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.materia import MateriaCreate, MateriaRead, MateriaUpdate
from app.services.materia_service import create_materia, get_materia, get_materias_by_instituicao, update_materia, delete_materia
from app.services.usuario_service import get_usuario_by_email
from app.services.instituicao_service import get_instituicao
from app.db.database import get_db
from app.core.auth import decode_token
from app.models.instituicao import Instituicao
from app.models.usuario import Usuario
from app.models.materia import Materia

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

router = APIRouter(prefix="/subject", tags=["Matéria"])

async def get_current_user(token: str, db: AsyncSession) -> Usuario:
    """Verifica o token e retorna o usuário atual"""
    token_email = decode_token(token)
    if not token_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    current_user = await get_usuario_by_email(db, token_email)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return current_user

@router.post("/{instituition_id}", response_model=MateriaRead, status_code=status.HTTP_201_CREATED)
async def create_subject(instituition_id: int, materia: MateriaCreate, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)

        current_institution = await get_instituicao(db, instituition_id)
        if not current_institution:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituição not found")

        # Verificar se o usuário é dono da instituição
        if current_user.id != current_institution.usuario_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to create this subject")

        return await create_materia(db, materia, instituition_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/all/{instituition_id}", response_model=list[MateriaRead])
async def get_subjects_by_instituition(instituition_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)

        current_institution = await get_instituicao(db, instituition_id)
        if not current_institution:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituição not found")

        # Verificar se o usuário é dono da instituição
        if current_user.id != current_institution.usuario_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to view this subjects")

        return await get_materias_by_instituicao(db, instituition_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/{materia_id}", response_model=MateriaRead)
async def get_subject_by_id(materia_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)

        materia = await get_materia(db, materia_id)
        if not materia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matéria not found")

        current_institution = await get_instituicao(db, materia.instituicao_id)
        if not current_institution:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituição not found")
            
        # Verificar se o usuário é dono da instituição
        if current_user.id != current_institution.usuario_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to view this subject")

        return materia
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.put("/{materia_id}", response_model=MateriaRead)
async def update_subject(materia_id: int, materia_data: MateriaUpdate, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)

        # Primeiro verificar se a matéria existe
        materia = await get_materia(db, materia_id)
        if not materia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matéria not found")

        current_institution = await get_instituicao(db, materia.instituicao_id)
        if not current_institution:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituição not found")
            
        # Verificar se o usuário é dono da instituição
        if current_user.id != current_institution.usuario_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to update this subject")

        updated_materia = await update_materia(db, materia_id, materia_data)
        if not updated_materia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matéria not found")
        return updated_materia
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{materia_id}")
async def delete_subject(materia_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)

        # CORREÇÃO DO BUG CRÍTICO: Buscar a matéria primeiro, não a instituição pelo materia_id
        materia = await get_materia(db, materia_id)
        if not materia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matéria not found")

        current_institution = await get_instituicao(db, materia.instituicao_id)
        if not current_institution:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituição not found")
            
        # Verificar se o usuário é dono da instituição
        if current_user.id != current_institution.usuario_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to delete this subject")
        
        if await delete_materia(db, materia_id):
            return {"detail": "Matéria deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matéria not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))