from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.instituicao import InstituicaoCreate, InstituicaoRead, InstituicaoUpdate
from app.services.instituicao_service import create_instituicao, get_instituicao, get_instituicoes_by_usuario, update_instituicao, delete_instituicao
from app.services.usuario_service import get_usuario_by_email
from app.db.database import get_db
from app.core.auth import decode_token
from app.models.usuario import Usuario
from app.models.instituicao import Instituicao

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

router = APIRouter(prefix="/instituition", tags=["Instituição"])

async def get_current_user(token: str, db: AsyncSession) -> Usuario:
    """Verifica o token e retorna o usuário atual"""
    token_email = decode_token(token)
    if not token_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    current_user = await get_usuario_by_email(db, token_email)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return current_user

@router.post("/{user_id}", response_model=InstituicaoRead, status_code=status.HTTP_201_CREATED)
async def create_instituition(user_id: int, instituicao: InstituicaoCreate, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)
        
        # Verificar se o usuário pode criar instituição para este user_id
        if current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to create this institution")

        return await create_instituicao(db, instituicao, user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/all/{user_id}", response_model=list[InstituicaoRead])
async def get_instituitions_by_user(user_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)
        
        # Verificar se o usuário pode ver as instituições deste user_id
        if current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to view this institutions")

        return await get_instituicoes_by_usuario(db=db, usuario_id=user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{instituicao_id}", response_model=InstituicaoRead)
async def get_instituition_by_id(instituicao_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)

        instituicao = await get_instituicao(db, instituicao_id)
        if not instituicao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituição not found")
            
        # Verificar se o usuário é dono da instituição
        if current_user.id != instituicao.usuario_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to view this institution")

        return instituicao
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{instituicao_id}", response_model=InstituicaoRead)
async def update_instituition(instituicao_id: int, instituicao_data: InstituicaoUpdate, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)

        # Verificar se a instituição existe e se o usuário é o dono
        instituicao = await get_instituicao(db, instituicao_id)
        if not instituicao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituição not found")
            
        if current_user.id != instituicao.usuario_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to update this institution")

        updated_instituicao = await update_instituicao(db, instituicao_id, instituicao_data)
        if not updated_instituicao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituição not found")
        return updated_instituicao
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{instituicao_id}")
async def delete_instituition(instituicao_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)

        # Verificar se a instituição existe e se o usuário é o dono
        instituicao = await get_instituicao(db, instituicao_id)
        if not instituicao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituição not found")
            
        if current_user.id != instituicao.usuario_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to delete this institution")

        deleted = await delete_instituicao(db, instituicao_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituição not found")
        return {"detail": "Instituição deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

