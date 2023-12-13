# **Default Database Schema**

<img src="/docs/img/Group2_ERD.png" alt="Image">


## **The Schema Module**

1. The **`CLV_Analysis/DB/schema`** module defines the SQLAlchemy models representing entities in the company's database, including Product, Customer, Transaction, Date, and Sale. These models are used to interact with the underlying database and perform CRUD operations.

    **Classes:**

    - Product: Represents a product in the company.

    - Customer: Represents a customer in the company.

    - Transaction: Represents a transaction in the company.

    - Date: Represents a date in the company.

    - Sale: Represents a sale in the company.

    **Note:**

    - These classes are SQLAlchemy declarative base classes, allowing for easy interaction with the database through an ORM (Object-Relational Mapping).


## **Schema Building Guide**

* This script builds the database schema using the classes defined in the CLV_Analysis.DB.schema module.

* It imports all classes from the schema module to create the necessary tables for the SQLite database.

**Note:** The file containing the following script should be executed to set up the database schema.

```py
from CLV_Analysis.DB.schema import *
```

