from sqlalchemy.ext.asyncio import AsyncSession

async def add_and_commit(db: AsyncSession, instance):
    db.add(instance)
    await db.commit()
    await db.refresh(instance)
    return instance

async def get_by_id(db: AsyncSession, model, id):
    return await db.get(model, id)
