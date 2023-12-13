# **FastAPI Integration**

## Modules

1. The **`CLV_Analysis/API/models`** module defines Pydantic models for database entities, representing the data structures used in the FastAPI endpoints for the Sales Fact, Product, Customer, Transaction, and Date entities

2. The **`CLV_Analysis/API/main`** module defines FastAPI endpoints for interacting with Sales Fact, Product, Customer, Transaction, and Date entities. It utilizes a SQLite database for data storage and retrieval.

    **Endpoints:**

    - **`sales_fact`**: APIs for Sales Fact entity (create, read, update, delete).

    - **`product`**: APIs for Product entity (create, read, update, delete).

    - **`customer`**: APIs for Customer entity (create, read, update, delete).

    - **`transaction`**: APIs for Transaction entity (create, read, update, delete).

    - **`date`**: APIs for Date entity (create, read, update, delete).

    Each API endpoint supports standard CRUD operations and interacts with a SQLite database through the **`sql_interactions`** module.

## FastAPI Application Starting Guide

This script starts the FastAPI application using uvicorn and opens it in a web browser.

**Note:** Ensure that the uvicorn package is installed before running this script.

```py
import subprocess
import webbrowser
from CLV_Analysis.API import main
```
```py
def start_fastapi():
    subprocess.run(["uvicorn", "CLV_Analysis.API.main:app", "--reload"])
    webbrowser.open('http://127.0.0.1:8000/docs#/')

```
```py
name = "__main__"

if name == "__main__":
    start_fastapi()
```