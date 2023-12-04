from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_closed,
    check_project_invested,
    check_charity_project_exists,
    check_edit_full_amount)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate)
from app.services.investment import investment

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
        Создание проекта"""
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await investment(new_project, Donation, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Для всех пользователей.
    Получение списка всех проектов."""
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
        Редактирование проекта."""
    charity_project = await check_charity_project_exists(
        project_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    check_project_closed(charity_project)
    if obj_in.full_amount is not None:
        check_edit_full_amount(charity_project, obj_in)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session)
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
        Удаление проекта."""
    project = await check_charity_project_exists(
        project_id, session)
    check_project_invested(project)
    project = await charity_project_crud.remove(
        project, session)
    return project
