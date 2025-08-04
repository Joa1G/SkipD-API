from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.instituicao import Instituicao
from app.schemas.instituicao import InstituicaoCreate, InstituicaoUpdate
from app.services.usuario_service import get_usuario
from fastapi import HTTPException

async def create_instituicao(db: AsyncSession, instituicao: InstituicaoCreate, usuario_id: int):
    if not await get_usuario(db, usuario_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    instituicao_obj = Instituicao(**instituicao.model_dump(), usuario_id=usuario_id)
    db.add(instituicao_obj)
    await db.commit()
    await db.refresh(instituicao_obj)
    return instituicao_obj

async def get_instituicao(db: AsyncSession, instituicao_id: int):
    result = await db.execute(select(Instituicao).filter(Instituicao.id == instituicao_id))
    return result.scalar_one_or_none()

async def get_instituicoes_by_usuario(db: AsyncSession, usuario_id: int):
    result = await db.execute(select(Instituicao).filter(Instituicao.usuario_id == usuario_id))
    return result.scalars().all()

async def update_instituicao(db: AsyncSession, instituicao_id: int, instituicao_data: InstituicaoUpdate):
    instituicao = await get_instituicao(db, instituicao_id=instituicao_id)

    if instituicao:
        for field, value in instituicao_data.model_dump(exclude_unset=True).items():
            setattr(instituicao, field, value)
        await db.commit()
        await db.refresh(instituicao)
        return instituicao
    return None

async def delete_instituicao(db: AsyncSession, instituicao_id: int):
    instituicao = await get_instituicao(db, instituicao_id=instituicao_id)
    if instituicao:
        await db.delete(instituicao)
        await db.commit()
        return True
    return False