from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.materia import Materia
from app.schemas.materia import MateriaCreate, MateriaUpdate
from fastapi import HTTPException
from app.services.instituicao_service import get_instituicao

async def create_materia(db: AsyncSession, materia: MateriaCreate, instituicao_id: int):

    if not await get_instituicao(db, instituicao_id):
        raise HTTPException(status_code=404, detail="Instituição não encontrada")

    materia_obj = Materia(**materia.model_dump(), instituicao_id=instituicao_id)
    db.add(materia_obj)
    await db.commit()
    await db.refresh(materia_obj)
    return materia_obj

async def get_materia(db: AsyncSession, materia_id: int):
    result = await db.execute(select(Materia).filter(Materia.id == materia_id))
    return result.scalar_one_or_none()

async def get_materias_by_instituicao(db: AsyncSession, instituicao_id: int):
    result = await db.execute(select(Materia).filter(Materia.instituicao_id == instituicao_id))
    return result.scalars().all()

async def update_materia(db: AsyncSession, materia_id: int, materia_data: MateriaUpdate):
    materia = await get_materia(db, materia_id=materia_id)

    if materia:
        for field, value in materia_data.model_dump(exclude_unset=True).items():
            setattr(materia, field, value)
        await db.commit()
        await db.refresh(materia)
        return materia
    return None

async def delete_materia(db: AsyncSession, materia_id: int):
    materia = await get_materia(db, materia_id=materia_id)
    if materia:
        await db.delete(materia)
        await db.commit()
        return True
    return False