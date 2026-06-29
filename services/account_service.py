from sqlalchemy.orm import Session

from models import Customer
from models import Account


# --------------------------------
# Create Account
# --------------------------------

def create_account(

        db: Session,

        full_name: str,

        email: str,

        phone: str,

        account_number: int,

        balance: float

):

    # Check Account Number

    account = db.query(Account).filter(
        Account.account_number == account_number
    ).first()

    if account:

        return "Account Exists"

    # Create Customer

    customer = Customer(

        name=full_name,

        email=email,

        phone=phone

    )

    db.add(customer)

    db.commit()

    db.refresh(customer)

    # Create Account

    account = Account(

        account_number=account_number,

        customer_id=customer.customer_id,

        balance=balance

    )

    db.add(account)

    db.commit()

    db.refresh(account)

    return account


# --------------------------------
# Get Balance
# --------------------------------

def get_balance(

        db: Session,

        account_number: int

):

    account = db.query(Account).filter(

        Account.account_number == account_number

    ).first()

    return account