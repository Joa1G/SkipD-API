from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioLogin, UsuarioRead, UsuarioChangePassword
from app.core.auth import verify_password, get_password_hash, create_access_token

def create_usuario(db: Session, usuario_data: UsuarioCreate):
    usuario_dict = usuario_data.model_dump()
    usuario_dict['senha'] = get_password_hash(usuario_dict['senha'])

    usuario = Usuario(**usuario_dict)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def update_usuario(db: Session, usuario_id: int, usuario_data: UsuarioUpdate):
    usuario = get_usuario(db, usuario_id=usuario_id)

    if usuario:
        updates = usuario_data.model_dump(exclude_unset=True)

        if 'senha' in updates:
            updates['senha'] = get_password_hash(updates.pop('senha'))

        for field, value in updates.items():
            setattr(usuario, field, value)
        db.commit()
        db.refresh(usuario)
        return usuario
    return None

def delete_usuario(db: Session, usuario_id: int):
    usuario = get_usuario(db, usuario_id=usuario_id)
    if usuario:
        db.delete(usuario)
        db.commit()
        return True
    return False

def login_usuario(db: Session, credentials: UsuarioLogin):
    usuario = db.query(Usuario).filter(Usuario.email == credentials.email).first()

    if not usuario or not verify_password(credentials.senha, usuario.senha):
        return False
    
    token = create_access_token(data={"sub": usuario.email})
    usuario_data = UsuarioRead.model_validate(usuario)
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario_data
    }

def change_password(db: Session, usuario_id: int, password_data: UsuarioChangePassword):
    usuario = get_usuario(db, usuario_id=usuario_id)

    if not usuario or not verify_password(password_data.old_senha, usuario.senha):
        return False

    new_password_hash = get_password_hash(password_data.new_senha)
    usuario.senha = new_password_hash
    db.commit()
    db.refresh(usuario)
    return True
