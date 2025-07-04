from datetime import datetime
from sqlmodel import SQLModel, Field


class EventBase(SQLModel):
    description: str
    location: str
    date: datetime

class EventCreate(EventBase):
    pass

class EventPublic(EventBase):
    id: int

class Event(EventBase, table=True):
    id: int = Field(default=None, primary_key=True)

