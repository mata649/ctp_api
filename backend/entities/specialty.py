from cgitb import enable
import dataclasses
from typing import List


@dataclasses.dataclass
class Specialty:
    id: str = None
    title: str = None
    images: List[str] = None
    description: str = None
    recommended_skills: List[str] = None
    color: str = None
    enable: bool = True

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)

    def to_dict(self) -> dict:
        return{
            'id': self.id,
            'title': self.title,
            'images': self.images,
            'description': self.description,
            'recommended_skills': self.recommended_skills,
            'color': self.color,
            'enable': self.enable
        }
