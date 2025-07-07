from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(primary_key=True, min_length=3)
    name: str = Field(nullable=False, min_length=3)
    email: EmailStr = Field(nullable=False)

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    pass

class User(UserBase, table=True):
    pass
