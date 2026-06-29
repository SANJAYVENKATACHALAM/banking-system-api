from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime
)

from database import Base


# --------------------------------
# User
# --------------------------------

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )


# --------------------------------
# Customer
# --------------------------------

class Customer(Base):

    __tablename__ = "customers"

    customer_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        nullable=False
    )

    phone = Column(
        String(15),
        nullable=False
    )


# --------------------------------
# Account
# --------------------------------

class Account(Base):

    __tablename__ = "accounts"

    account_number = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id")
    )

    balance = Column(
        Float,
        default=0
    )


# --------------------------------
# Transaction
# --------------------------------

class Transaction(Base):

    __tablename__ = "transactions"

    transaction_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    account_number = Column(
        Integer,
        ForeignKey("accounts.account_number")
    )

    transaction_type = Column(
        String(20)
    )

    amount = Column(
        Float
    )

    transaction_date = Column(
        DateTime,
        default=datetime.now
    )