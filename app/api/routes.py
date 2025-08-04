from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from app.schemas.usuario import UsuarioLogin
from app.services.usuario_service import login_usuario

security = HTTPBearer()
router = APIRouter()

@router.get("/secure-endpoint", dependencies=[Depends(security)])
def secure_endpoint():
    return {"message": "Entrou"}

@router.post("/token")
async def login_usuario_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # OAuth2PasswordRequestForm usa 'username' como campo, mas tratamos como email
    usuario_input = UsuarioLogin(email=form_data.username, senha=form_data.password)
    usuario = await login_usuario(db, usuario_input)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return usuario
