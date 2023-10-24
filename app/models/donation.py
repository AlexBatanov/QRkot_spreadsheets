from sqlalchemy import Column, Integer, Text, ForeignKey

from app.models.abstract import AbstractModel


class Donation(AbstractModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=True)
