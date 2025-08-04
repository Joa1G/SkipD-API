from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate, UsuarioChangePassword
from app.services.usuario_service import create_usuario, get_usuario, get_usuario_by_email, update_usuario, delete_usuario, change_password
from app.db.database import get_db
from app.core.auth import decode_token
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/user", tags=["Usuario"])

async def get_current_user(token: str, db: AsyncSession) -> Usuario:
    """Verifica o token e retorna o usuário atual"""
    token_email = decode_token(token)
    if not token_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    current_user = await get_usuario_by_email(db, token_email)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return current_user

@router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_usuario(db, user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/{user_id}", response_model=UsuarioRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)
        
        # Verificar se o usuário pode acessar este perfil
        if current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")
        
        usuario = await get_usuario(db, user_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return usuario
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.put("/{user_id}", response_model=UsuarioRead)
async def update_user(user_id: int, user: UsuarioUpdate, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)
        
        # Verificar se o usuário pode atualizar este perfil
        if current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

        updated = await update_usuario(db, user_id, user)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)
        
        # Verificar se o usuário pode deletar este perfil
        if current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

        deleted = await delete_usuario(db, user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"detail": "User deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{user_id}/change-password")
async def change_user_password(user_id: int, password_data: UsuarioChangePassword, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        current_user = await get_current_user(token, db)
        
        # Verificar se o usuário pode alterar a senha deste perfil
        if current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

        success = await change_password(db, user_id, password_data)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password or user not found")
        return {"detail": "Password changed successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
