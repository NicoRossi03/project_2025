from typing import Annotated

from http.client import HTTPException

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlmodel import select, Session
from sqlalchemy import delete

from app.config import config
from app.data.db import get_session
from app.models.event import Event, EventCreate
from app.models.registration import Registration
from app.models.user import User, UserPublic, UserCreate

router = APIRouter()
templates = Jinja2Templates(directory=config.root_dir / "templates")
SessionDep = Annotated[Session, Depends(get_session)]
@router.get("/users")
async def get_all_users(session: SessionDep):
    return session.exec(select(User)).all()

@router.post("/users")
async def add_user(session: SessionDep, data: UserCreate):
    session.add(User.model_validate(data))
    session.commit()
    return {"ok": True, "message": "User added"}

@router.get("/users/{username}")
async def get_user_by_username(session: SessionDep, username: str):
    user = session.get(User, username)
    if user is None:
        raise HTTPException(status_code=404, detail={"ok": False})
    else:
        return user
@router.delete("/users")
async def delete_all_users(session: SessionDep):
    session.exec(delete(User))
    session.commit()
    return {"ok": True, "message": "Users deleted"}

@router.delete("/users/{username}")
async def delete_user_by_username(session: SessionDep, username: str):
    res = session.exec(delete(User).where(User.username == username))
    session.commit()
    if res.rowcount > 0:
        return {"ok": True, "message": "User deleted"}
    else:
        raise HTTPException(status_code=404, detail={"ok": False, "message": "User not found"})

@router.get("/events")
async def get_all_events(session: SessionDep):
    return session.exec(select(Event)).all()

@router.post("/events")
async def add_event(session: SessionDep, data: EventCreate):
    session.add(Event.model_validate(data))
    session.commit()
    return {"ok": True, "message": "Event added"}

@router.get("/events/{id}")
async def get_event_by_id(session: SessionDep, id: int):
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail={"ok": False})
    else:
        return event

@router.put("/events/{id}")
async def add_event(session: SessionDep, data: EventCreate, id: int):
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail={"ok": False, "message": "Event not found"})

    new_event_data = Event.model_validate(data)

    event.title = new_event_data.title
    event.description = new_event_data.description
    event.location = new_event_data.location
    event.date = new_event_data.date

    session.add(event)
    session.commit()
    return {"ok": True, "message": "Event updated"}

@router.delete("/events")
async def delete_all_events(session: SessionDep):
    session.exec(delete(Event))
    session.commit()
    return {"ok": True, "message": "Events deleted"}





@router.delete("/events/{id}")
async def delete_event_by_id(session: SessionDep, id: int):
    res = session.exec(delete(Event).where(Event.id == id))
    session.commit()
    if res.rowcount > 0:
        return {"ok": True, "message": "Event deleted"}
    else:
        raise HTTPException(status_code=404, detail={"ok": False, "message": "Event not found"})

@router.post("/events/{event_id}/register")
async def add_registration(session: SessionDep, data: UserPublic, event_id: int):
    try:
        user = User.model_validate(data)  # sfruttiamo il fatto che usercreate e userpublic coincidono
        session.add(
            Registration(username=user.username, event_id=event_id)
        )
        session.commit()
    except ValidationError:
        raise HTTPException(status_code=400, detail={"ok": False, "message": "invalid payload format"})
    except Exception as e:
        raise HTTPException(status_code=404, detail={"ok": False, "message": "user not found"})
    else:
        return {"ok": True, "message": "Registration added"}

@router.get("/registrations")
async def get_all_registrations(session: SessionDep):
    return session.exec(select(Registration)).all()

@router.delete("/registrations")
async def delete_event_by_id(session: SessionDep, username: str, event_id: str):
    res = session.exec(delete(Registration).where(Registration.username == username, Registration.event_id == event_id))
    session.commit()
    if res.rowcount > 0:
        return {"ok": True, "message": "Registration deleted"}
    else:
        raise HTTPException(status_code=404, detail={"ok": False, "message": "Registration not found"})
