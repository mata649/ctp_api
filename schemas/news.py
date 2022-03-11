from email.policy import default
from typing import Optional
from pydantic import BaseModel, Field
import datetime


class BaseNews(BaseModel):
    id: Optional[str] = Field(default=None)
    title: str = Field(...)
    text: str = Field(...)
    published: Optional[datetime.datetime] = Field(default=None)


class NewsIn(BaseNews):
    class Config:
        schema_extra = {
            "example": {
                "title": "Arreglo de Uniformes",
                "text": "lorem ipsun text lorem ipsun textlorem ipsun textlorem ipsun textlorem ipsun textlorem ipsun textlorem ipsun textlorem ipsun textlorem ipsun textlorem ipsun textlorem ipsun textlorem ipsun text",
            }
        }

class NewsOut(BaseNews):
    pass