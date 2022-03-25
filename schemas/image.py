import imp
from pydantic import BaseModel, Field


class ImageIn(BaseModel):
    image_encoded: str = Field(...)
