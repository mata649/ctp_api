import dataclasses
from typing import List


@dataclasses.dataclass
class Workshop:
    id: str = None
    title: str = None
    images: List[str] = None
    description: str = None
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
            'color': self.color,
            'enable': self.enable
        }
