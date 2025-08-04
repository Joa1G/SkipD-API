from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_db, Session
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from app.schemas.usuario import UsuarioLogin
from app.services.usuario_service import login_usuario

security = HTTPBearer()
router = APIRouter()

@router.get("/secure-endpoint", dependencies=[Depends(security)])
def secure_endpoint():
    return {"message": "Entrou"}

@router.post("/token")
def login_usuario_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario_input = UsuarioLogin(email=form_data.email, senha=form_data.password)
    usuario = login_usuario(db, usuario_input)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return usuario
