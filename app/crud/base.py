from typing import Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.validators import check_name_duplicate, validate_delete_obj

from app.models.user import User
from app.services.services import invested_amount


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get_multi(
        self, session: AsyncSession, user: Union[User, None] = None
    ):
        """Получение списка объектов"""
        if user:
            donations = await session.execute(
                select(self.model).where(self.model.user_id == user.id)
            )
            return donations.scalars().all()
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create_project(
        self, obj,
        session: AsyncSession,
        user: Optional[User] = None
    ):
        """Создание объекта"""
        obj_in_data = obj.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        if obj_in_data.get('name') is not None:
            await check_name_duplicate(obj_in_data.get('name'), session)
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return await invested_amount(db_obj, session)

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        """Удаление объекта"""
        db_obj = await validate_delete_obj(db_obj)
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_obj(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        """Получение объекта"""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()
