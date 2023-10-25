from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.crud.constants import PROJECT_NOT_FOUND
from app.models.charity_project import CharityProject


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
