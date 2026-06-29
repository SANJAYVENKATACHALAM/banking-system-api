from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from services.account_service import (
    create_account,
    get_balance
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# --------------------------------
# Dashboard
# --------------------------------

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request
        }
    )


# --------------------------------
# Create Account Page
# --------------------------------

@router.get("/create-account", response_class=HTMLResponse)
def create_account_page(request: Request):

    return templates.TemplateResponse(
        "create_account.html",
        {
            "request": request
        }
    )


# --------------------------------
# Create Account
# --------------------------------

@router.post("/create-account", response_class=HTMLResponse)
def create_new_account(

        request: Request,

        full_name: str = Form(...),

        email: str = Form(...),

        phone: str = Form(...),

        account_number: int = Form(...),

        balance: float = Form(...),

        db: Session = Depends(get_db)

):

    account = create_account(
        db,
        full_name,
        email,
        phone,
        account_number,
        balance
    )

    if account == "Account Exists":

        return templates.TemplateResponse(
            "create_account.html",
            {
                "request": request,
                "error": "Account Number Already Exists"
            }
        )

    return templates.TemplateResponse(
        "create_account.html",
        {
            "request": request,
            "success": "Account Created Successfully",
            "account": account,
            "customer_name": full_name,
            "email": email,
            "phone": phone
        }
    )


# --------------------------------
# Balance Page
# --------------------------------

@router.get("/balance", response_class=HTMLResponse)
def balance_page(request: Request):

    return templates.TemplateResponse(
        "balance.html",
        {
            "request": request
        }
    )


# --------------------------------
# Check Balance
# --------------------------------

@router.post("/balance", response_class=HTMLResponse)
def check_balance(

        request: Request,

        account_number: int = Form(...),

        db: Session = Depends(get_db)

):

    account = get_balance(
        db,
        account_number
    )

    if account is None:

        return templates.TemplateResponse(
            "balance.html",
            {
                "request": request,
                "error": "Account Not Found"
            }
        )

    return templates.TemplateResponse(
        "balance.html",
        {
            "request": request,
            "account": account
        }
    )