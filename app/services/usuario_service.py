from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioLogin, UsuarioRead, UsuarioChangePassword
from app.core.auth import verify_password, get_password_hash, create_access_token

async def create_usuario(db: AsyncSession, usuario_data: UsuarioCreate):
    usuario_dict = usuario_data.model_dump()
    usuario_dict['senha'] = get_password_hash(usuario_dict['senha'])

    usuario = Usuario(**usuario_dict)
    db.add(usuario)
    await db.commit()
    await db.refresh(usuario)
    return usuario

async def get_usuario(db: AsyncSession, usuario_id: int):
    result = await db.execute(select(Usuario).filter(Usuario.id == usuario_id))
    return result.scalar_one_or_none()

async def get_usuario_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Usuario).filter(Usuario.email == email))
    return result.scalar_one_or_none()

async def update_usuario(db: AsyncSession, usuario_id: int, usuario_data: UsuarioUpdate):
    usuario = await get_usuario(db, usuario_id=usuario_id)

    if usuario:
        updates = usuario_data.model_dump(exclude_unset=True)

        if 'senha' in updates:
            updates['senha'] = get_password_hash(updates.pop('senha'))

        for field, value in updates.items():
            setattr(usuario, field, value)
        await db.commit()
        await db.refresh(usuario)
        return usuario
    return None

async def delete_usuario(db: AsyncSession, usuario_id: int):
    usuario = await get_usuario(db, usuario_id=usuario_id)
    if usuario:
        await db.delete(usuario)
        await db.commit()
        return True
    return False

async def login_usuario(db: AsyncSession, credentials: UsuarioLogin):
    usuario = await get_usuario_by_email(db, credentials.email)

    if not usuario or not verify_password(credentials.senha, usuario.senha):
        return False
    
    token = create_access_token(data={"sub": usuario.email})
    usuario_data = UsuarioRead.model_validate(usuario)
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario_data
    }

async def change_password(db: AsyncSession, usuario_id: int, password_data: UsuarioChangePassword):
    usuario = await get_usuario(db, usuario_id=usuario_id)

    if not usuario or not verify_password(password_data.old_senha, usuario.senha):
        return False

    new_password_hash = get_password_hash(password_data.new_senha)
    usuario.senha = new_password_hash
    await db.commit()
    await db.refresh(usuario)
    return True

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(Usuario))
    return result.scalars().all()