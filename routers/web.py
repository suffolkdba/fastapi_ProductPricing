from fastapi import FastAPI, HTTPException, APIRouter, Request, Form, Depends
from sqlmodel import Session
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import get_session
from routers.products import add_product

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", 
                                      {"request": request})

