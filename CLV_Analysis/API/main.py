"""
API Module

This module defines FastAPI endpoints for interacting with various entities
including Sales Fact, Product, Customer, Transaction, and Date. It utilizes
a SQL database for data storage and retrieval.

Endpoints:
- /sales_fact: APIs for Sales Fact entity (create, read, update, delete).
- /product: APIs for Product entity (create, read, update, delete).
- /customer: APIs for Customer entity (create, read, update, delete).
- /transaction: APIs for Transaction entity (create, read, update, delete).
- /date: APIs for Date entity (create, read, update, delete).

Each API endpoint supports standard CRUD operations and interacts with a SQL
database through the sql_interactions module.

Note:
- Ensure the proper configuration of the database connection in sql_interactions.
- This module assumes the use of FastAPI and requires appropriate model definitions.

"""

from fastapi import FastAPI, HTTPException
from ..DB import sql_interactions
from .models import (
    SalesFactCreate, SalesFactUpdate,
    ProductCreate, ProductUpdate,
    CustomerCreate, CustomerUpdate,
    TransactionCreate, TransactionUpdate,
    DateCreate, DateUpdate
)

app = FastAPI()

# Sales Fact API Methods


@app.post("/sales_fact/")
async def create_sales_fact(insert_values: SalesFactCreate):
    """
    Create a new sales fact record.

    Parameters:
    - `insert_values`: The data to insert for the new sales fact.

    Returns:
    - The created sales fact.
    """
    try:
        db_sales = sql_interactions.SqlHandler.insert_by_id(
            insert_values,
            db_name="temp.db", table_name="sales_fact"
        )
        return db_sales
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.get("/sales_fact/")
async def select_sales_facts(start_id: int, head: int):
    """
    Select multiple sales facts within a range.

    Parameters:
    - `start_id`: The starting ID of the range.
    - `head`: The number of records to retrieve.

    Returns:
    - List of selected sales facts.
    """
    try:
        db_sales_fact = sql_interactions.SqlHandler.select_many(
            start_id, head,
            db_name="temp.db", table_name="sales_fact", table_id="sales_id"
        )
        return db_sales_fact
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.get("/sales_fact/{sales_fact_id}")
async def select_sales_fact(sales_fact_id: int):
    """
    Select a specific sales fact by ID.

    Parameters:
    - `sales_fact_id`: The ID of the sales fact to retrieve.

    Returns:
    - The selected sales fact.
    """
    try:
        db_sales_fact = sql_interactions.SqlHandler.select_by_id(
            sales_fact_id,
            db_name="temp.db", table_name='sales_fact', table_id="sales_id"
        )
        return db_sales_fact
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.put("/sales_fact/{sales_fact_id}")
async def update_sales_fact(row_id: int, update_data: SalesFactUpdate):
    """
    Update a sales fact record by ID.

    Parameters:
    - `row_id`: The ID of the sales fact to update.
    - `update_data`: The data to update for the sales fact.

    Returns:
    - The result of the update operation.
    """
    try:
        result = sql_interactions.SqlHandler.update_by_id(
            row_id, update_data,
            db_name="temp.db", table_name="sales_fact", table_id="sales_id"
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )


@app.delete("/sales_fact/{sales_fact_id}")
async def delete_sales_fact(sales_fact_id: int):
    """
    Delete a sales fact record by ID.

    Parameters:
    - `sales_fact_id`: The ID of the sales fact to delete.

    Returns:
    - The result of the delete operation.
    """
    try:
        db_sales_fact = sql_interactions.SqlHandler.delete_by_id(
            sales_fact_id,
            db_name="temp.db", table_name='sales_fact', table_id="sales_id"
        )
        return db_sales_fact
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )

# Product API Methods


@app.post("/product/")
async def create_product(insert_values: ProductCreate):
    """
    Delete a sales fact record by ID.

    Parameters:
    - `sales_fact_id`: The ID of the sales fact to delete.

    Returns:
    - The result of the delete operation.
    """
    try:
        db_product = sql_interactions.SqlHandler.insert_by_id(
            insert_values,
            db_name="temp.db", table_name="product"
        )
        return db_product
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.get("/product/")
async def select_products(start_id: int, head: int):
    """
    Select multiple products within a range.

    Parameters:
    - `start_id`: The starting ID of the range.
    - `head`: The number of records to retrieve.

    Returns:
    - List of selected products.
    """
    try:
        db_products = sql_interactions.SqlHandler.select_many(
            start_id, head,
            db_name="temp.db", table_name="product", table_id="product_id"
        )
        return db_products
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.get("/product/{product_id}")
async def select_product(product_id: int):
    """
    Select a specific product by ID.

    Parameters:
    - `product_id`: The ID of the product to retrieve.

    Returns:
    - The selected product.
    """
    try:
        db_product = sql_interactions.SqlHandler.select_by_id(
            product_id,
            db_name="temp.db", table_name='product', table_id="product_id"
        )
        return db_product
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.put("/product/{product_id}")
async def update_product(row_id: int, update_data: ProductUpdate):
    """
    Update a product record by ID.

    Parameters:
    - `row_id`: The ID of the product to update.
    - `update_data`: The data to update for the product.

    Returns:
    - The result of the update operation.
    """
    try:
        result = sql_interactions.SqlHandler.update_by_id(
            row_id, update_data,
            db_name="temp.db", table_name="product", table_id="product_id"
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )


@app.delete("/product/{product_id}")
async def delete_product(product_id: int):
    """
    Delete a product record by ID.

    Parameters:
    - `product_id`: The ID of the product to delete.

    Returns:
    - The result of the delete operation.
    """
    try:
        db_product = sql_interactions.SqlHandler.delete_by_id(
            product_id,
            db_name="temp.db", table_name='product', table_id="product_id"
        )
        return db_product
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )

# Customer API Methods


@app.post("/customer/")
async def create_customer(insert_values: CustomerCreate):
    """
    Create a new customer record.

    Parameters:
    - `insert_values`: The data to insert for the new customer.

    Returns:
    - The created customer.
    """
    try:
        db_customer = sql_interactions.SqlHandler.insert_by_id(
            insert_values,
            db_name="temp.db", table_name="customer"
        )
        return db_customer
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.get("/customer/")
async def select_customers(start_id: int, head: int):
    """
    Select multiple customers within a range.

    Parameters:
    - `start_id`: The starting ID of the range.
    - `head`: The number of records to retrieve.

    Returns:
    - List of selected customers.
    """
    try:
        db_customers = sql_interactions.SqlHandler.select_many(
            start_id, head,
            db_name="temp.db", table_name="customer", table_id="customer_id"
        )
        return db_customers
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.get("/customer/{customer_id}")
async def select_customer(customer_id: int):
    """
    Select a specific customer by ID.

    Parameters:
    - `customer_id`: The ID of the customer to retrieve.

    Returns:
    - The selected customer.
    """
    try:
        db_customer = sql_interactions.SqlHandler.select_by_id(
            customer_id,
            db_name="temp.db", table_name='customer', table_id="customer_id"
        )
        return db_customer
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.put("/customer/{customer_id}")
async def update_customer(row_id: int, update_data: CustomerUpdate):
    """
    Update a customer record by ID.

    Parameters:
    - `row_id`: The ID of the customer to update.
    - `update_data`: The data to update for the customer.

    Returns:
    - The result of the update operation.
    """
    try:
        result = sql_interactions.SqlHandler.update_by_id(
            row_id, update_data,
            db_name="temp.db", table_name="customer", table_id="customer_id"
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )


@app.delete("/customer/{customer_id}")
async def delete_customer(customer_id: int):
    """
    Delete a customer record by ID.

    Parameters:
    - `customer_id`: The ID of the customer to delete.

    Returns:
    - The result of the delete operation.
    """
    try:
        db_customer = sql_interactions.SqlHandler.delete_by_id(
            customer_id,
            db_name="temp.db", table_name='customer', table_id="customer_id"
        )
        return db_customer
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )

# Transaction API Methods


@app.post("/transaction/")
async def create_transaction(insert_values: TransactionCreate):
    """
    Create a new transaction record.

    Parameters:
    - `insert_values`: The data to insert for the new transaction.

    Returns:
    - The created transaction.
    """
    try:
        db_transaction = sql_interactions.SqlHandler.insert_by_id(
            insert_values,
            db_name="temp.db", table_name="transactions"
        )
        return db_transaction
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.get("/transaction/")
async def select_transactions(start_id: int, head: int):
    """
    Select multiple transactions within a range.

    Parameters:
    - `start_id`: The starting ID of the range.
    - `head`: The number of records to retrieve.

    Returns:
    - List of selected transactions.
    """
    try:
        db_transactions = sql_interactions.SqlHandler.select_many(
            start_id, head,
            db_name="temp.db", table_name="transactions",
            table_id="transaction_id"
        )
        return db_transactions
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.get("/transaction/{transaction_id}")
async def select_transaction(transaction_id: int):
    """
    Select a specific transaction by ID.

    Parameters:
    - `transaction_id`: The ID of the transaction to retrieve.

    Returns:
    - The selected transaction.
    """
    try:
        db_transaction = sql_interactions.SqlHandler.select_by_id(
            transaction_id,
            db_name="temp.db", table_name='transactions',
            table_id="transaction_id"
        )
        return db_transaction
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.put("/transaction/{transaction_id}")
async def update_transaction(row_id: int, update_data: TransactionUpdate):
    """
    Update a transaction record by ID.

    Parameters:
    - `row_id`: The ID of the transaction to update.
    - `update_data`: The data to update for the transaction.

    Returns:
    - The result of the update operation.
    """
    try:
        result = sql_interactions.SqlHandler.update_by_id(
            row_id, update_data,
            db_name="temp.db", table_name="transactions",
            table_id="transaction_id"
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )


@app.delete("/transaction/{transaction_id}")
async def delete_transaction(transaction_id: int):
    """
    Delete a transaction record by ID.

    Parameters:
    - `transaction_id`: The ID of the transaction to delete.

    Returns:
    - The result of the delete operation.
    """
    try:
        db_transaction = sql_interactions.SqlHandler.delete_by_id(
            transaction_id,
            db_name="temp.db", table_name='transactions',
            table_id="transaction_id"
        )
        return db_transaction
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )

# Date API Methods


@app.post("/date/")
async def create_date(insert_values: DateCreate):
    """
    Create a new date record.

    Parameters:
    - `insert_values`: The data to insert for the new date.

    Returns:
    - The created date.
    """
    try:
        db_date = sql_interactions.SqlHandler.insert_by_id(
            insert_values,
            db_name="temp.db", table_name="date"
        )
        return db_date
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.get("/date/")
async def select_dates(start_id: int, head: int):
    """
    Select multiple dates within a range.

    Parameters:
    - `start_id`: The starting ID of the range.
    - `head`: The number of records to retrieve.

    Returns:
    - List of selected dates.
    """
    try:
        db_dates = sql_interactions.SqlHandler.select_many(
            start_id, head,
            db_name="temp.db", table_name="date", table_id="date_id"
        )
        return db_dates
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.get("/date/{date_id}")
async def select_date(date_id: int):
    """
    Select a specific date by ID.

    Parameters:
    - `date_id`: The ID of the date to retrieve.

    Returns:
    - The selected date.
    """
    try:
        db_date = sql_interactions.SqlHandler.select_by_id(
            date_id,
            db_name="temp.db", table_name='date', table_id="date_id"
        )
        return db_date
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


@app.put("/date/{date_id}")
async def update_date(row_id: int, update_data: DateUpdate):
    """
    Update a date record by ID.

    Parameters:
    - `row_id`: The ID of the date to update.
    - `update_data`: The data to update for the date.

    Returns:
    - The result of the update operation.
    """
    try:
        result = sql_interactions.SqlHandler.update_by_id(
            row_id, update_data,
            db_name="temp.db", table_name="date", table_id="date_id"
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )


@app.delete("/date/{date_id}")
async def delete_date(date_id: int):
    """
    Delete a date record by ID.

    Parameters:
    - `date_id`: The ID of the date to delete.

    Returns:
    - The result of the delete operation.
    """
    try:
        db_date = sql_interactions.SqlHandler.delete_by_id(
            date_id,
            db_name="temp.db", table_name='date', table_id="date_id"
        )
        return db_date
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )
