from datetime import datetime

from sqlalchemy import (
    Column, Integer, Boolean, CheckConstraint, DateTime
)

from app.crud.constants import DEFAULT_AMOUNT, MIN_AMOUNT
from app.core.db import Base


class AbstractModel(Base):
    __abstract__ = True

    full_amount = Column(
        Integer, CheckConstraint(f'full_amount >= {MIN_AMOUNT}'), nullable=False
    )
    invested_amount = Column(
        Integer, CheckConstraint(f'invested_amount >= {MIN_AMOUNT}'),
        default=DEFAULT_AMOUNT, nullable=False
    )
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None, nullable=True)
