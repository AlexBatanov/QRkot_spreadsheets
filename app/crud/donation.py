from app.crud.base import CRUDBase
from app.models.donation import Donation


class DonationProject(CRUDBase):
    """CRUD класс фонда"""


donation_crud = DonationProject(Donation)
