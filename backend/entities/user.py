import dataclasses
from .roles import Roles

@dataclasses.dataclass
class User:
    id: str = None
    email: str = None
    full_name: str = None
    password: str = None
    role: Roles = 'EDITOR'
    enable: bool = None

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)

    def to_dict(self) -> dict:
        return{
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "password": self.password,
            "role": self.role,
            "enable": self.enable
        }
