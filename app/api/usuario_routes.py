from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate, UsuarioChangePassword
from app.services.usuario_service import create_usuario, get_usuario, get_usuario_by_email, update_usuario, delete_usuario, change_password, get_all_users
from app.db.database import get_db
from app.core.auth import decode_token, verify_password
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

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
        
        if user.email:
            existing_user_with_email = await db.scalar(select(Usuario).where(Usuario.email == user.email, Usuario.id != user_id))
            if existing_user_with_email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

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
    
@router.get("", response_model=list[UsuarioRead])
async def list_all_users(db: AsyncSession = Depends(get_db)):
    try:
        users = await get_all_users(db)
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/check-email")
async def check_email_availability(email_data: dict, db: AsyncSession = Depends(get_db)):
    """Verifica se email está em uso"""
    try:
        email = email_data.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
            
        user = await get_usuario_by_email(db, email)
        return {"email_in_use": user is not None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}/premium")
async def toggle_premium_status(user_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Alterna status premium do usuário"""
    try:
        current_user = await get_current_user(token, db)
        
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Access forbidden")
        
        user = await get_usuario(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        user.is_premium = not user.is_premium
        await db.commit()
        await db.refresh(user)
        
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify-password")
async def verify_user_password(password_data: dict, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Verifica se a senha está correta"""
    try:
        current_user = await get_current_user(token, db)
        password = password_data.get("password")
        
        if not password:
            raise HTTPException(status_code=400, detail="Password is required")
            
        is_valid = verify_password(password, current_user.senha)
        return {"is_valid": is_valid}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
