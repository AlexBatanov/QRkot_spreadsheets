from pydantic import BaseModel, HttpUrl

from app.crud.constants import RESPONSE_URL


class GoogleSheetURL(BaseModel):
    url: HttpUrl

    class Config:
        schema_extra = {
            "example": {
                "url": RESPONSE_URL
            }
        }
