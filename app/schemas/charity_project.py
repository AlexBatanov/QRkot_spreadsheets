from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt

from app.crud.constants import MIN_LENGHT, MAX_LENGHT


class CharityProjectCreate(BaseModel):
    name: str
    description: str
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        min_anystr_length = MIN_LENGHT
        max_anystr_length = MAX_LENGHT


class CharityProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = MIN_LENGHT
        max_anystr_length = MAX_LENGHT


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class CharityProjectGetUpdate(CharityProjectDB):
    pass


class CharityProjectGetDelete(CharityProjectDB):
    pass
