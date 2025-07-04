from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: int

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
