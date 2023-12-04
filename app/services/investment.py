from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def close_donat(object):
    """Процесс закрытия проекта/пожертвования."""
    object.fully_invested = True
    object.invested_amount = object.full_amount
    object.close_date = datetime.now()
    return object


async def investment(
    donats, project, session: AsyncSession
):
    """Процесс пожертвования."""
    objects = await session.execute(
        select(project).where(
            project.fully_invested == 0
        ).order_by(project.create_date)
    )
    objects = objects.scalars().all()
    for object in objects:
        free_amount_donat = donats.full_amount - donats.invested_amount
        free_amount_project = object.full_amount - object.invested_amount
        if free_amount_donat > free_amount_project:
            donats.invested_amount += free_amount_project
            await close_donat(object)
        if free_amount_donat == free_amount_project:
            await close_donat(donats)
            await close_donat(object)
        else:
            object.invested_amount += free_amount_donat
            await close_donat(donats)
    session.add_all((*objects, donats))
    await session.commit()
    await session.refresh(donats)
    return donats
