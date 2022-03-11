from enum import Enum


class Roles(str, Enum):
    ADMIN = "ADMIN"
    GENERAL = "EDITOR"
    SUPERADMIN = "SUPERADMIN"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
