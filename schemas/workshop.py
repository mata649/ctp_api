from typing import Optional, List
from pydantic import BaseModel, Field

class BaseWorkshop(BaseModel):
    id: Optional[str] = Field(default=None)
    title: str = Field(...)
    images: Optional[List[str]] = Field(default=[])
    description: str = Field(...)
    color: str = Field(..., max_length=8)

class WorkshopIn(BaseWorkshop):
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Muebles",
                "images": ["img1","img2"],
                "description": "Descripcion de la especialidad",
                "recommended_skills": ["Proactivo", "Analitico", "Trabajo en equipo"],
                "color" : "#42d369"
            }
        }

class WorkshopOut(BaseWorkshop):
    pass