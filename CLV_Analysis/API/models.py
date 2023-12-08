"""
Models Module

This module defines Pydantic models for database entities, representing the
data structures used in the FastAPI endpoints for the Sales Fact, Product,
Customer, Transaction, and Date entities.

Models:
- ProductCreate: Pydantic model for creating a new product.
- ProductUpdate: Pydantic model for updating an existing product.
- CustomerCreate: Pydantic model for creating a new customer.
- CustomerUpdate: Pydantic model for updating an existing customer.
- TransactionCreate: Pydantic model for creating a new transaction.
- TransactionUpdate: Pydantic model for updating an existing transaction.
- DateCreate: Pydantic model for creating a new date.
- DateUpdate: Pydantic model for updating an existing date.
- SalesFactCreate: Pydantic model for creating a new sales fact.
- SalesFactUpdate: Pydantic model for updating an existing sales fact.

Each model corresponds to a database entity and includes the necessary fields
with their respective types. Optional fields are provided for update operations.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Pydantic models for database entities


class ProductCreate(BaseModel):
    """
    Pydantic model for creating a new product.

    Fields:
    - `SKU`: Stock Keeping Unit for the product.
    - `product_category`: Category of the product.
    - `producer_country`: Country where the product is produced.
    - `price`: Price of the product.
    """
    SKU: str
    product_category: str
    producer_country: str
    price: float


class ProductUpdate(BaseModel):
    """
    Pydantic model for updating an existing product.

    Optional Fields:
    - `SKU`: Stock Keeping Unit for the product.
    - `product_category`: Category of the product.
    - `producer_country`: Country where the product is produced.
    - `price`: Price of the product.
    """
    SKU: Optional[str] = None
    product_category: Optional[str] = None
    producer_country: Optional[str] = None
    price: Optional[float] = None


class CustomerCreate(BaseModel):
    """
    Pydantic model for creating a new customer.

    Fields:
    - `customer_name`: First name of the customer.
    - `customer_surname`: Last name of the customer.
    - `email`: Email address of the customer.
    - `phone`: Phone number of the customer.
    - `country`: Country of residence.
    - `city`: City of residence.
    - `address`: Address of the customer.
    - `zip_code`: ZIP code of the customer's location.
    - `birthday`: Date of birth of the customer.
    - `gender`: Gender of the customer.
    """
    customer_name: str
    customer_surname: str
    email: str
    phone: str
    country: str
    city: str
    address: str
    zip_code: str
    birthday: datetime
    gender: str


class CustomerUpdate(BaseModel):
    """
    Pydantic model for updating an existing customer.

    Optional Fields:
    - `customer_name`: First name of the customer.
    - `customer_surname`: Last name of the customer.
    - `email`: Email address of the customer.
    - `phone`: Phone number of the customer.
    - `country`: Country of residence.
    - `city`: City of residence.
    - `address`: Address of the customer.
    - `zip_code`: ZIP code of the customer's location.
    - `birthday`: Date of birth of the customer.
    - `gender`: Gender of the customer.
    """
    customer_name: Optional[str] = None
    customer_surname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    birthday: Optional[datetime] = None
    gender: Optional[str] = None


class TransactionCreate(BaseModel):
    """
    Pydantic model for creating a new transaction.

    Fields:
    - `date`: Date of the transaction.
    - `payment_method`: Payment method used for the transaction.
    - `customer_id`: ID of the customer associated with the transaction.
    """
    date: datetime
    payment_method: str
    customer_id: int


class TransactionUpdate(BaseModel):
    """
    Pydantic model for updating an existing transaction.

    Optional Fields:
    - `date`: Date of the transaction.
    - `payment_method`: Payment method used for the transaction.
    - `customer_id`: ID of the customer associated with the transaction.
    """
    date: Optional[datetime] = None
    payment_method: Optional[str] = None
    customer_id: Optional[int] = None


class DateCreate(BaseModel):
    """
    Pydantic model for creating a new date.

    Fields:
    - `date`: Date.
    - `month`: Month of the date.
    - `month_name`: Name of the month.
    - `year`: Year of the date.
    - `quarter`: Quarter of the year.
    - `day_of_month`: Day of the month.
    - `day_of_year`: Day of the year.
    - `day_of_week_number`: Day of the week (number).
    - `day_of_week_name`: Name of the day of the week.
    - `week_of_year`: Week of the year.
    - `week_of_month`: Week of the month.
    """
    date: datetime
    month: int
    month_name: str
    year: int
    quarter: int
    day_of_month: int
    day_of_year: int
    day_of_week_number: int
    day_of_week_name: str
    week_of_year: int
    week_of_month: int


class DateUpdate(BaseModel):
    """
    Pydantic model for updating an existing date.

    Optional Fields:
    - `date`: Date.
    - `month`: Month of the date.
    - `month_name`: Name of the month.
    - `year`: Year of the date.
    - `quarter`: Quarter of the year.
    - `day_of_month`: Day of the month.
    - `day_of_year`: Day of the year.
    - `day_of_week_number`: Day of the week (number).
    - `day_of_week_name`: Name of the day of the week.
    - `week_of_year`: Week of the year.
    - `week_of_month`: Week of the month.
    """
    date: Optional[datetime] = None
    month: Optional[int] = None
    month_name: Optional[str] = None
    year: Optional[int] = None
    quarter: Optional[int] = None
    day_of_month: Optional[int] = None
    day_of_year: Optional[int] = None
    day_of_week_number: Optional[int] = None
    day_of_week_name: Optional[str] = None
    week_of_year: Optional[int] = None
    week_of_month: Optional[int] = None


class SalesFactCreate(BaseModel):
    """
    Pydantic model for creating a new sales fact.

    Fields:
    - `transaction_id`: ID of the associated transaction.
    - `product_id`: ID of the associated product.
    - `customer_id`: ID of the associated customer.
    - `quantity`: Quantity sold.
    - `date_id`: ID of the associated date.
    """
    transaction_id: int
    product_id: int
    customer_id: int
    quantity: int
    date_id: int


class SalesFactUpdate(BaseModel):
    """
    Pydantic model for updating an existing sales fact.

    Optional Fields:
    - `transaction_id`: ID of the associated transaction.
    - `product_id`: ID of the associated product.
    - `customer_id`: ID of the associated customer.
    - `quantity`: Quantity sold.
    - `date_id`: ID of the associated date.
    """
    transaction_id: Optional[int] = None
    product_id: Optional[int] = None
    customer_id: Optional[int] = None
    quantity: Optional[int] = None
    date_id: Optional[int] = None
