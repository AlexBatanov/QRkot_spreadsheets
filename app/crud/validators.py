from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate
from app.crud.constants import (
    MIN_AMOUNT,
    NAME_NOT_UNIQUE,
    PROJECT_NOT_FOUND,
    AMOUNT_LESS_THAN_INVETED,
    CLOSED_PROJECT_DONT_REDACTED,
    INVESTED_PROJECT_DONT_DELETE
)


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка на уникальность имени"""
    from app.crud.charity_project import charityproject_crud
    project_id = await charityproject_crud.get_project_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NAME_NOT_UNIQUE,
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка на существование объекта"""
    from app.crud.charity_project import charityproject_crud
    charity_project = await charityproject_crud.get_obj(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return charity_project


def check_charity_project_closed(
        charity_project: CharityProject,
        error_msg: str
) -> None:
    """Проверка на закрытие фонда (полностью проинвестирован)"""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=error_msg
        )


def check_charity_project_invested_amount(
        charity_project: CharityProject,
        error_msg: str
) -> None:
    """Проверка на внесенные инвестиции"""
    if charity_project.invested_amount > MIN_AMOUNT:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=error_msg
        )


def chek_new_full_amount(
    obj_in,
    project: CharityProject
) -> None:
    """Проверка финальной суммы фонда (не должна быть меньше инвестиций)"""
    new_amount = obj_in.full_amount
    if new_amount is not None:
        if new_amount < project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=AMOUNT_LESS_THAN_INVETED
            )


async def validate_update_data(
    charity_project: CharityProject,
    obj_in: CharityProjectUpdate,
    session: AsyncSession
) -> CharityProject:
    """Проверка обновленных данных для фонда"""
    check_charity_project_closed(charity_project, CLOSED_PROJECT_DONT_REDACTED)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    chek_new_full_amount(obj_in, charity_project)
    return charity_project


async def validate_delete_obj(project: CharityProject) -> CharityProject:
    """Проверка на возможность удаление фонда"""
    check_charity_project_closed(project, INVESTED_PROJECT_DONT_DELETE)
    check_charity_project_invested_amount(
        project, INVESTED_PROJECT_DONT_DELETE
    )
    return project
