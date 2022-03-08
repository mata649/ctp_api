import dataclasses
from datetime import datetime


@dataclasses.dataclass
class News:
    id: str = None
    title: str = None
    text: str = None
    user_id: str = None
    published: datetime = None
    enable: bool = True

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)

    def to_dict(self) -> dict:
        return{
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'user_id': self.user_id,
            'published': self.published,
            'enable': self.enable
        }
