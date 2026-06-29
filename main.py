from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import engine, Base
from models import User, Account, Transaction

from routers import users
from routers import accounts
from routers import transactions

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banking Management System"
)

# HTML Templates
templates = Jinja2Templates(directory="templates")

# Static Folder
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# Include Routers
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(transactions.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )