from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charityproject_crud
from app.core.user import current_superuser
from app.crud.validators import check_charity_project_exists
from app.schemas.charity_project import (
    CharityProjectDB, CharityProjectCreate,
    CharityProjectUpdate, CharityProjectGetUpdate,
    CharityProjectGetDelete
)

router = APIRouter()


@router.get(
    '/', response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session)
):
    """Получение всех фондов"""
    return await charityproject_crud.get_multi(session)


@router.post(
    '/', response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создание нового фонда, только для суперюзера"""
    return await charityproject_crud.create_project(project, session)


@router.delete(
    '/{charity_project_id}',
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectGetDelete,
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Удаление фонда, только для суперюзера"""
    project = await check_charity_project_exists(charity_project_id, session)
    return await charityproject_crud.remove(project, session)


@router.patch(
    '/{project_id}', response_model=CharityProjectGetUpdate,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Обновление фонда, только для суперюзера"""
    project = await check_charity_project_exists(project_id, session)
    return await charityproject_crud.update(
        project, obj_in, session
    )
