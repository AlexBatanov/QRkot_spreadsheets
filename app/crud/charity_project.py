from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.crud.validators import validate_update_data
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):
    """CRUD класс фонда"""

    async def get_project_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ):
        """Получение объекта по имени"""
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name
            )
        )
        return db_project.scalars().first()

    async def update(
        self,
        project: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession
    ):
        """Обновление объекта"""
        await validate_update_data(
            project, obj_in, session
        )
        obj_data = jsonable_encoder(project)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(project, field, update_data[field])
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project


charityproject_crud = CRUDCharityProject(CharityProject)
