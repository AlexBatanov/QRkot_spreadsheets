from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.models.user import User
from app.core.user import current_user, current_superuser
from app.schemas.donation import (
    DonationCreate, DonationUser, DonationDB
)


router = APIRouter()


@router.get(
    '/', response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
) -> list[DonationDB]:
    """Получение всех пожертований, только для суперюзера"""
    return await donation_crud.get_multi(session)


@router.post(
    '/', response_model=DonationUser,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def create_donations(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> DonationUser:
    """Создание пожертвования"""
    return await donation_crud.create_project(donation, session, user)


@router.get('/my', response_model=list[DonationUser])
async def get_me_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> list[DonationUser]:
    """Получение всех пожертвований пользователя"""
    return await donation_crud.get_multi(session, user)
