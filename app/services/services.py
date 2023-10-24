from datetime import datetime
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def get_list_closed_objects(
        session: AsyncSession,
        model: Union[Donation, CharityProject] = CharityProject,
        fully: bool = False
) -> list[Union[Donation, CharityProject]]:
    """
    По умолчанию возвращает список открытых проектов или пожертований.
    Для получения закрытых парметр fully=True
    """
    all_objects = await session.execute(
        select(model).where(model.fully_invested == fully)
    )
    return all_objects.scalars().all()


async def invested_amount(
    invest_obj: Union[Donation, CharityProject],
    session: AsyncSession,
    model=Donation
) -> Union[Donation, CharityProject]:
    """
    Инвестирование в проект

    при создании фонда получаем выборку с открытыми донатами,
    происходит пополнение фонда и закрытие инвестиций,
    пока сумма фонда не будет покрыта
    или пока есть пожертвования

    при создание пожертвования получаем выборку с откытами фондами,
    происходит пополнение фондов пока не кончится сумма инвестиций
    или пока есть фонды
    """
    if isinstance(invest_obj, Donation):
        model = CharityProject

    all_objects = await get_list_closed_objects(session, model)

    for obj in all_objects:
        free_amount = obj.full_amount - obj.invested_amount
        need_amount = invest_obj.full_amount - invest_obj.invested_amount
        if need_amount < free_amount:
            obj.invested_amount += need_amount
            update_cur_obj(invest_obj)
        elif need_amount == free_amount:
            update_cur_obj(invest_obj)
            update_cur_obj(obj)
        else:
            invest_obj.invested_amount += free_amount
            update_cur_obj(obj)
        session.add(obj)

    session.add(invest_obj)
    await session.commit()
    await session.refresh(invest_obj)
    return invest_obj


def update_cur_obj(obj):
    """Обновления объекта до статуса 'full_invested = True'"""
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()
