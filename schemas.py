from pydantic import BaseModel


# ---------- User ----------

class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# ---------- Account ----------

class AccountCreate(BaseModel):
    account_number: int


class BalanceResponse(BaseModel):
    account_number: int
    balance: float


# ---------- Transaction ----------

class TransactionRequest(BaseModel):
    account_number: int
    amount: float