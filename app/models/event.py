from sqlmodel import SQLModel, Field


class Event(SQLModel, table=True):
    id: int = Field(primary_key=True)
