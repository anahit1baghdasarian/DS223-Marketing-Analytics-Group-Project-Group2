"""
Database Models Module

This module defines the SQLAlchemy models representing entities in the company's database,
including Product, Customer, Transaction, Date, and Sale. These models are used to interact
with the underlying database and perform CRUD operations.

Classes:
- Product: Represents a product in the company.
- Customer: Represents a customer in the company.
- Transaction: Represents a transaction in the company.
- Date: Represents a date in the company.
- Sale: Represents a sale in the company.

Note:
- These classes are SQLAlchemy declarative base classes, allowing for easy interaction
  with the database through an ORM (Object-Relational Mapping).
"""

import logging
from ..Logger.logger import CustomFormatter
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

engine = create_engine('sqlite:///temp.db')
Base = declarative_base()


class Product(Base):
    """
    Represents a product in the company.

    Attributes:
    - product_id: Primary key identifying the product.
    - SKU: Stock Keeping Unit for the product.
    - product_category: Category of the product.
    - producer_country: Country where the product is produced.
    - price: Price of the product.
    """
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    SKU = Column(String)
    product_category = Column(String)
    producer_country = Column(String)
    price = Column(Float)


class Customer(Base):
    """
    Represents a customer in the company.

    Attributes:
    - customer_id: Primary key identifying the customer.
    - customer_name: Name of the customer.
    - customer_surname: Surname of the customer.
    - email: Email address of the customer.
    - phone: Phone number of the customer.
    - country: Country where the customer is located.
    - city: City where the customer is located.
    - address: Address of the customer.
    - zip_code: ZIP code of the customer.
    - birthday: Birthday of the customer.
    - gender: Gender of the customer.
    """
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    customer_surname = Column(String)
    email = Column(String)
    phone = Column(String)
    country = Column(String)
    city = Column(String)
    address = Column(String)
    zip_code = Column(String)
    birthday = Column(DateTime)
    gender = Column(String)


class Transaction(Base):
    """
    Represents a transaction in the company.

    Attributes:
    - transaction_id: Primary key identifying the transaction.
    - date: Date of the transaction.
    - payment_method: Payment method used for the transaction.
    - customer_id: Foreign key linking to the Customer entity.
    """
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    payment_method = Column(String)

    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    customers = relationship("Customer", backref="transactions")


class Date(Base):
    """
    Represents a date in the company.

    Attributes:
    - date_id: Primary key identifying the date.
    - date: Date value.
    - month: Month of the date.
    - month_name: Name of the month.
    - year: Year of the date.
    - quarter: Quarter of the date.
    - day_of_month: Day of the month.
    - day_of_year: Day of the year.
    - day_of_week_number: Day of the week (numeric representation).
    - day_of_week_name: Name of the day of the week.
    - week_of_year: Week of the year.
    - week_of_month: Week of the month.
    """
    __tablename__ = "date"

    date_id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    month = Column(Integer)
    month_name = Column(String)
    year = Column(Integer)
    quarter = Column(Integer)
    day_of_month = Column(Integer)
    day_of_year = Column(Integer)
    day_of_week_number = Column(Integer)
    day_of_week_name = Column(String)
    week_of_year = Column(Integer)
    week_of_month = Column(Integer)


class Sale(Base):
    """
    Represents a sale in the company.

    Attributes:
    - sales_id: Primary key identifying the sale.
    - transaction_id: Foreign key linking to the Transaction entity.
    - product_id: Foreign key linking to the Product entity.
    - customer_id: Foreign key linking to the Customer entity.
    - quantity: Quantity of the product sold in the sale.
    - date_id: Foreign key linking to the Date entity.
    """
    __tablename__ = "sales_fact"

    sales_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.transaction_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    quantity = Column(Integer)
    date_id = Column(Integer, ForeignKey('date.date_id'))

    transaction = relationship("Transaction")
    product = relationship("Product")
    customer = relationship("Customer")
    date = relationship("Date")


Base.metadata.create_all(engine)
