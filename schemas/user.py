from cgitb import enable
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class Role(str, Enum):
    ADMIN = "ADMIN"
    GENERAL = "EDITOR"
    SUPERADMIN = "SUPERADMIN"


class UserBase(BaseModel):
    id: Optional[str] = Field(default=None)
    email: EmailStr = Field(...)
    full_name: str = Field(..., max_length=80)
    role: Role = Field(...)
    enable: bool = Field(default=True)



class UserIn(UserBase):
    password: str = Field(..., max_length=64)

    class Config:
        schema_extra = {
            "example": {
                "role": "EDITOR",
                "email": "example@example.com",
                "full_name": "Example Name",
                "password": "Example"
            }
        }
class UserOut(UserBase):
    pass


class UserLoginIn(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=64)


class UserLoginOut(UserBase):
    jwt: str = Field(default=None)

class UserUpdateIn(BaseModel):
    email: EmailStr
    full_name: str = Field(..., max_length=80)
    role: Role
    

    class Config:
        schema_extra = {
            "example": {
                "role": "EDITOR",
                "email": "example@example.com",
                "full_name": "Example Name",
            }
        }

class UserUpdateOut(UserBase):
    pass

class UserChangePasswordIn(BaseModel):
    password: str = Field(..., max_length=64)

class UserChangePasswordOut(BaseModel):
    pass