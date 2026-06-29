from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from services.user_service import create_user, authenticate_user
from auth import create_access_token

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ------------------------------------
# Register Page
# ------------------------------------
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse(
        "register.html",
        {
            "request": request
        }
    )


# ------------------------------------
# Register User
# ------------------------------------
@router.post("/register")
def register(

    username: str = Form(...),

    password: str = Form(...),

    db: Session = Depends(get_db)

):

    create_user(
        db,
        username,
        password
    )

    return RedirectResponse(
        url="/login",
        status_code=303
    )


# ------------------------------------
# Login Page
# ------------------------------------
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request
        }
    )


# ------------------------------------
# Login User
# ------------------------------------
@router.post("/login")
def login(

    request: Request,

    username: str = Form(...),

    password: str = Form(...),

    db: Session = Depends(get_db)

):

    db_user = authenticate_user(
        db,
        username,
        password
    )

    if db_user is None:

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid Username or Password"
            }
        )

    token = create_access_token(
        {
            "sub": db_user.username
        }
    )

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )