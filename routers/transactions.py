from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from services.transaction_service import (
    deposit_money,
    withdraw_money,
    get_transactions
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# --------------------------------
# Deposit Page
# --------------------------------

@router.get("/deposit", response_class=HTMLResponse)
def deposit_page(request: Request):

    return templates.TemplateResponse(
        "deposit.html",
        {
            "request": request
        }
    )


# --------------------------------
# Deposit Money
# --------------------------------

@router.post("/deposit", response_class=HTMLResponse)
def deposit(

        request: Request,

        account_number: int = Form(...),

        amount: float = Form(...),

        db: Session = Depends(get_db)

):

    account = deposit_money(
        db,
        account_number,
        amount
    )

    if account is None:

        return templates.TemplateResponse(
            "deposit.html",
            {
                "request": request,
                "error": "Account Not Found"
            }
        )

    return templates.TemplateResponse(
        "deposit.html",
        {
            "request": request,
            "success": "Amount Deposited Successfully",
            "account": account
        }
    )


# --------------------------------
# Withdraw Page
# --------------------------------

@router.get("/withdraw", response_class=HTMLResponse)
def withdraw_page(request: Request):

    return templates.TemplateResponse(
        "withdraw.html",
        {
            "request": request
        }
    )


# --------------------------------
# Withdraw Money
# --------------------------------

@router.post("/withdraw", response_class=HTMLResponse)
def withdraw(

        request: Request,

        account_number: int = Form(...),

        amount: float = Form(...),

        db: Session = Depends(get_db)

):

    account = withdraw_money(
        db,
        account_number,
        amount
    )

    if account is None:

        return templates.TemplateResponse(
            "withdraw.html",
            {
                "request": request,
                "error": "Account Not Found"
            }
        )

    if account == "Insufficient Balance":

        return templates.TemplateResponse(
            "withdraw.html",
            {
                "request": request,
                "error": "Insufficient Balance"
            }
        )

    return templates.TemplateResponse(
        "withdraw.html",
        {
            "request": request,
            "success": "Withdrawal Successful",
            "account": account
        }
    )


# --------------------------------
# Transaction History Page
# --------------------------------

@router.get("/transactions", response_class=HTMLResponse)
def transaction_page(request: Request):

    return templates.TemplateResponse(
        "transactions.html",
        {
            "request": request
        }
    )


# --------------------------------
# Transaction History
# --------------------------------

@router.post("/transactions", response_class=HTMLResponse)
def transaction_history(

        request: Request,

        account_number: int = Form(...),

        db: Session = Depends(get_db)

):

    transactions = get_transactions(
        db,
        account_number
    )

    if not transactions:

        return templates.TemplateResponse(
            "transactions.html",
            {
                "request": request,
                "error": "No Transactions Found",
                "account_number": account_number
            }
        )

    return templates.TemplateResponse(
        "transactions.html",
        {
            "request": request,
            "transactions": transactions,
            "account_number": account_number
        }
    )