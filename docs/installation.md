# **CLV Analysis Package User Guide**

## **Introduction 👋**

Welcome to the CLV_Analysis package!🤗 

This package is designed to facilitate Customer Lifetime Value (CLV) analysis in the retail domain.🛒🛍️ 

By leveraging this package, you can gain valuable insights into customer behavior and make informed decisions to maximize long-term profitability. 📊📈📉🎯


## **Table of Contents 🤓**

- [**Logger Module**](logger.md)
    - [Classes](logger.md#classes)
    - [Usage](logger.md#usage)
    - [Example](logger.md#example)
    - [Note](logger.md#note)
- [**Default Database Schema**](db_schema.md)
    - [The Schema Module](db_schema.md#the-schema-module)
    - [Schema Building Guide](db_schema.md#schema-building-guide)
- [**Synthetic Data for the Default Database**](synthetic_data.md)
    - [The Data Generator Module](synthetic_data.md#the-data-generator-module)
        - [Functions](synthetic_data.md#functions)
    - [Synthetic Data Generation Guide](synthetic_data.md#synthetic-data-generation-guide)
- [**The SqlHandler() and SQL Queries**](sql_interactions.md)
    - [SQLite Database Handler Module](sql_interactions.md#sqlite-database-handler-module)
        - [SqlHandler()](sql_interactions.md#sqlhandler)
    - [Queries to Test the Functionality of the Database](sql_interactions.md#queries-to-test-the-functionality-of-the-database)
- [**Data Insertion Guide**](data_insertion.md)
    - [The Modules](data_insertion.md#the-modules)
    - [Insertion Into The Tables](data_insertion.md#insertion-into-the-tables)
- [**FastAPI Integration**](fast_api.md)
    - [The Modules](fast_api.md#modules)
    - [FastAPI Application Starting Guide](fast_api.md#fastapi-application-starting-guide)
- [**CLTVModel() Class**](cltv_model.md#cltvmodel()-class)
- [**Complete Analysis with CLTVModel() Class**](clv_complete.md)
    - [Importing the Class and Making an Instance](clv_complete.md#importing-the-class-and-making-an-instance)
    - [What is Customer Lifetime Value(CLV)?](clv_complete.md#what-is-customer-lifetime-valueclv)
    - [CLV Prediction with BG-NBD and Gamma-Gamma](clv_complete.md#clv-prediction-with-bg-nbd-and-gamma-gamma)

## **Installation 📥**

```py
pip install clv_analysis

```

## **Testing the CLV_Analysis Package Step-by-Step 👣**

To ensure the proper functioning of the CLV_Analysis package, follow these steps:

1. **Create a SQLite DB Schema:**

    - Utilize the documentation in [DB Schema](db_schema.md) section to create a SQLite database schema for the analysis.

2. **Generate Synthetic Data:**

    - Use the documentation in [Synthetic Data](synthetic_data.md) section to create synthetic data for customers, products, transactions, dates, and sales.

3. **Insert Synthetic Data into the SQLite DB Schema:**

    - Insert the generated synthetic data into the SQLite database using the provided insertion guides in the [Data Insertion](data_insertion.md) section.

4. **Run Queries to Test Database Functionality:**

    - Test the functionality of the database by running queries. Refer to the [SQL Interactions](sql_interactions.md) section for guidance.

5. **Open Swagger in API:**

    - Start the FastAPI application to open Swagger UI. For guidance refer to the [FastAPI Integration](fast_api.md) section.

6. **Perform CRUD Operations with FastAPI:**

    - Use the provided CRUD tools to perform Create, Read, Update, and Delete operations on the database.

    - Follow the [FastAPI Integration](fast_api.md) section for assistance.

7. **Check Local Database for Modifications:**

    - Verify the modifications made through FastAPI by inspecting your local SQLite database.

8. **Import the CLTVModel() Class:**

    - Import the CLTVModel() class into your Python environment.
    - Follow the [Complete CLV Analysis](clv_complete.md) section for assistance.

9. **Perform Analysis using CLTVModel() Class:**

    - Utilize the CLTVModel() class to conduct a comprehensive Customer Lifetime Value analysis.
    - Follow the [Complete CLV Analysis](clv_complete.md) section for step-by-step guidance.

*By following these steps, you can ensure that the CLV_Analysis package is set up correctly and functions as intended.*

## **Troubleshooting 🎯**

If you encounter any issues, reach out to our team.

## **Contributing 🤝**

We welcome contributions! Feel free to submit bug reports, feature requests, or contribute to the codebase on our [GitHub repository](https://github.com/anahit1baghdasarian/DS223-Marketing-Analytics-Group-Project-Group2).

## **Contact Information 📞**

For further assistance or inquiries, contact our support team at 

- [@anahit_baghdasaryan2@edu.aua.am](mailto:anahit_baghdasaryan3@edu.aua.am)
- [@natela_azoyan@edu.aua.am](mailto:natela_azoyan@edu.aua.am)
- [@lilit_galstyan@edu.aua.am](mailto:lilit_galstyan@edu.aua.am)
- [@ofelya_stepanyan@edu.aua.am](mailto:ofelya_stepanyan@edu.aua.am)
- [@narek_khachikyan@edu.aua.am](mailto:narek_khachikyan@edu.aua.am)
