from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    is_premium: bool
    url_foto: str

class UsuarioRead(BaseModel):
    id: int
    nome: str
    email: EmailStr
    is_premium: bool
    url_foto: str

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    is_premium: Optional[bool] = None
    url_foto: Optional[str] = None

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class UsuarioChangePassword(BaseModel):
    old_senha: str
    new_senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

