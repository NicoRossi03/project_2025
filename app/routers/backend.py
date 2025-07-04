from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import config


router = APIRouter()
templates = Jinja2Templates(directory=config.root_dir / "templates")
