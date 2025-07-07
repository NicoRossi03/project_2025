from datetime import datetime
from sqlmodel import SQLModel, Field


class EventBase(SQLModel):
    title: str = Field(min_length=3, nullable=False)
    description: str = Field(min_length=3, nullable=False)
    location: str = Field(min_length=3, nullable=False)
    date: datetime = Field(nullable=False)

class EventCreate(EventBase):
    pass

class EventPublic(EventBase):
    id: int

class Event(EventBase, table=True):
    id: int = Field(default=None, primary_key=True)

