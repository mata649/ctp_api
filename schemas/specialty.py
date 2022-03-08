from typing import Optional, List
from pydantic import BaseModel, Field



class BaseSpecialty(BaseModel):
    id: Optional[str] = Field(default=None)
    title: str = Field(..., )
    images: Optional[List[str]] = Field(default=[])
    description: str = Field(..., )
    recommended_skills: Optional[List[str]] = Field(default=[])
    color: str = Field(..., max_length=8)

class SpecialtyIn(BaseSpecialty):
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Informatica Empresarial",
                "images": ["img1","img2"],
                "description": "Descripcion de la especialidad",
                "recommended_skills": ["Proactivo", "Analitico", "Trabajo en equipo"],
                "color" : "#42d369"
            }
        }

class SpecialtyOut(BaseSpecialty):
    pass