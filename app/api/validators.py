from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (
    CHECK_NAME_DUPLICATE,
    PROJECT_NOT_FOUND,
    CHECK_PROJECT_CLOSED,
    CHECK_EDIT_FULL_AMOUNT,
    CANNOT_BE_DELETED)
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CHECK_NAME_DUPLICATE,)


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return project


def check_project_closed(
    project: CharityProject
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CHECK_PROJECT_CLOSED
        )


def check_edit_full_amount(
    project: CharityProject, obj_in: CharityProject
) -> CharityProject:
    if obj_in.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CHECK_EDIT_FULL_AMOUNT
        )
    return project


def check_project_invested(
    project: CharityProject
) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CANNOT_BE_DELETED
        )
