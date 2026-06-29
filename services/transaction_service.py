from datetime import datetime
from sqlalchemy.orm import Session

from models import Account, Transaction


# --------------------------------
# Deposit Money
# --------------------------------

def deposit_money(
        db: Session,
        account_number: int,
        amount: float
):

    account = db.query(Account).filter(
        Account.account_number == account_number
    ).first()

    if account is None:
        return None

    account.balance = account.balance + amount

    transaction = Transaction(
        account_number=account.account_number,
        transaction_type="Deposit",
        amount=amount,
        transaction_date=datetime.now()
    )

    db.add(transaction)

    db.commit()

    db.refresh(account)

    return account


# --------------------------------
# Withdraw Money
# --------------------------------

def withdraw_money(
        db: Session,
        account_number: int,
        amount: float
):

    account = db.query(Account).filter(
        Account.account_number == account_number
    ).first()

    if account is None:
        return None

    if account.balance < amount:
        return "Insufficient Balance"

    account.balance = account.balance - amount

    transaction = Transaction(
        account_number=account.account_number,
        transaction_type="Withdraw",
        amount=amount,
        transaction_date=datetime.now()
    )

    db.add(transaction)

    db.commit()

    db.refresh(account)

    return account


# --------------------------------
# Transaction History
# --------------------------------

def get_transactions(
        db: Session,
        account_number: int
):

    return db.query(Transaction).filter(
        Transaction.account_number == account_number
    ).order_by(
        Transaction.transaction_date.desc()
    ).all()