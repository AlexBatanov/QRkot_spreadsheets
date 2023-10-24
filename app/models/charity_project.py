from sqlalchemy import Column, String, Text

from app.models.abstract import AbstractModel
from app.crud.constants import MAX_LENGHT


class CharityProject(AbstractModel):
    name = Column(String(MAX_LENGHT), unique=True, nullable=False)
    description = Column(Text, nullable=False)
