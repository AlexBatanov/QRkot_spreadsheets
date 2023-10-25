from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from aiogoogle import Aiogoogle

from app.core.config import settings
from app.services.services import get_list_closed_objects
from app.models.charity_project import CharityProject
from app.crud.constants import (
    FORMAT, ROW_COUNT,
    COLUMN_COUNT, SHEET_ID,
    SHEET_URL
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создание google таблицы"""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчет от {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': SHEET_ID,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': ROW_COUNT,
                                                      'columnCount': COLUMN_COUNT}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Установка доступа для чтения таблицы"""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """Заполнение таблицы закрытыми проектами"""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        new_row = [str(project.name),
                   str(project.close_date - project.create_date),
                   str(project.description)]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )


async def get_projects_by_completion_rate(
        session: AsyncSession
) -> list[CharityProject]:
    """
    Возвращает список проектов
    отсортированный по скорости сбору средств
    """
    all_projects = await get_list_closed_objects(session, fully=True)
    return sorted(
        all_projects,
        key=lambda obj: obj.create_date - obj.close_date,
        reverse=True
    )


async def create_update_google_table(
        wrapper_services: Aiogoogle,
        session: AsyncSession
) -> dict:
    """Создание, заполнение таблицы и выдача разрешения"""
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    projects = await get_projects_by_completion_rate(session)
    await spreadsheets_update_value(spreadsheetid, projects, wrapper_services)
    return {'url': SHEET_URL + spreadsheetid}
