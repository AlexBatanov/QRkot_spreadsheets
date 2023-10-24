from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from aiogoogle import Aiogoogle

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.services.google_client import create_update_google_table
from app.schemas.google_client import GoogleSheetURL

router = APIRouter()


@router.get(
    '/',
    response_model=GoogleSheetURL,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    """Создание таблицы с закрытыми проектами и получение id таблицы"""
    return await create_update_google_table(wrapper_services, session)
