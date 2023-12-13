# **Synthetic Data for the Default Database**

## **The Data Generator Module**

The `CLV_Analysis/DB/data_generator` module provides functions for generating synthetic data for the Sales Fact, Product, Customer,Transaction, and Date entities. It uses the Faker library to generate realistic fake data for testing and development purposes.

### **Functions:**

- **`generate_product`**: Generates fake data for a product.

    ```py
    generate_product(product_id)
    ```
    **Parameters:** **`product_id`**: ID of the product.

    **Returns:** Dictionary containing fake data for a product.

------------------------------------------------------------------

- **`generate_customer`**: Generates fake data for a customer.

    ```py
    generate_customer(customer_id)
    ```
    **Parameters:** **`customer_id`**: ID of the customer.

    **Returns:** Dictionary containing fake data for a customer.

------------------------------------------------------------------

- **`generate_transaction`**: Generates fake data for a transaction.

    ```py
    generate_transaction(transaction_id)
    ```
    **Parameters:** **`transaction_id`**: ID of the transaction.

    **Returns:** Dictionary containing fake data for a transaction.

------------------------------------------------------------------

- **`generate_date`**: Generates fake data for a date.
    
    ```py
    generate_date(date_id)
    ```

    **Parameters:** **`date_id`**: ID of the date.

    **Returns:** Dictionary containing fake data for a date.

------------------------------------------------------------------

- **`generate_sales`**: Generates fake data for sales.  

    ```py
    generate_sales()
    ```
    **Returns:** Dictionary containing fake data for sales.

------------------------------------------------------------------

**Note:**

- The functions in this module are intended for testing and development purposes, and the generated data may not reflect real-world scenarios.


## **Synthetic Data Generation Guide**

**This script generates sample data for Customer Lifetime Value (CLV) analysis**

### Loading Modules and Packages

- Import modules and packages necessary for data generation.

```py
from CLV_Analysis.DB.data_generator import generate_product
from CLV_Analysis.DB.data_generator import generate_customer
from CLV_Analysis.DB.data_generator import generate_transaction
from CLV_Analysis.DB.data_generator import generate_date
from CLV_Analysis.DB.data_generator import generate_sales
from datetime import datetime
import pandas as pd
import random
import os
```

### Declare Constants

- Define constants for the number of products, customers, and transactions.

```py
NUMBER_OF_PRODUCTS=5000
NUMBER_OF_CUSTOMERS=3000
NUMBER_OF_TRANSACTIONS=4000
```

### Create "data_csv" Folder, If It Doesn't Already Exist

```py
# Check if 'data_csv' folder exists, if not, create it
output_directory = 'data_csv'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)
```

### Generate Customer Data

- Generate customer data using the `generate_customer` function and save it to a CSV file.

```py
customer_data = [generate_customer(customer_id) for customer_id
                 in range(NUMBER_OF_CUSTOMERS)]

# Save customer data to CSV file in the 'data_csv' folder
output_file_path = os.path.join(output_directory, 'customer.csv')

pd.DataFrame(customer_data).to_csv(output_file_path, index=False)
```

### Generate Product Data

- Generate product data using the `generate_product` function and save it to a CSV file.

```py
product_data = [generate_product(product_id) for product_id
                in range(NUMBER_OF_PRODUCTS)]

# Save product data to CSV file in the 'data_csv' folder
output_file_path = os.path.join(output_directory, 'product.csv')

pd.DataFrame(product_data).to_csv(output_file_path, index=False)
```

### Generate Transaction Data

- Generate transaction data using the `generate_transaction` function and save it to a CSV file.

```py
transaction_data = [generate_transaction(transaction_id)
                    for transaction_id
                    in range(NUMBER_OF_TRANSACTIONS)] 

# Save transaction data to CSV file in the 'data_csv' folder
output_file_path = os.path.join(output_directory, 'transactions.csv')

pd.DataFrame(transaction_data).to_csv(output_file_path, index=False)
```

### Generate Dates Data

- Generate date data using the `generate_date` function and save it to a CSV file.

```py
# Define the start and end dates as strings
start_date = "2000-01-01"
end_date = "2023-12-31"

# Convert the date strings to datetime objects
start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

# Calculate the difference between the two dates
number_of_days = (end_date_obj - start_date_obj).days

dates_data = [generate_date(date_id) for date_id
              in range(number_of_days+1)] 

# Save date data to CSV file in the 'data_csv' folder
output_file_path = os.path.join(output_directory, 'date.csv')
pd.DataFrame(dates_data).to_csv(output_file_path, index=False)
```

### Generating Sales Data

- Generate sales data by associating transactions with products, customers, and dates.

- Save the sales data to a CSV file.

```py
# Convert 'date' columns in both DataFrames to datetime format
DateData = pd.DataFrame(dates_data)
TransData = pd.DataFrame(transaction_data)

DateData["date"] = pd.to_datetime(DateData["date"])
TransData["date"] = pd.to_datetime(TransData["date"])
```
```py
# Create an array with numbers from 1 to 4000
original_array = list(range(0, NUMBER_OF_TRANSACTIONS))

# Create a new array with randomly duplicated elements
duplicated_array = []

for num in original_array:

    # Generate a random number between 1 and 5 (inclusive)
    duplicates = random.randint(1, 5)

    # Append the number to the new array 'duplicates' times
    duplicated_array.extend([num] * duplicates)
```
```py
# Save sales data to CSV file in the 'data_csv' folder
output_file_path = os.path.join(output_directory, 'sales.csv')

# Create a DataFrame with sales data 
sales_data = [generate_sales() for i in range(len(duplicated_array))] 
sales_data = pd.DataFrame(sales_data)

# Generate a 'transaction_id' column
sales_data["transaction_id"] = duplicated_array

# Select relevant columns for the sales_data DataFrame
sales_data = sales_data[['transaction_id', 'product_id', 'quantity']]

# Merge sales_data with transaction and date information
sales_data = sales_data.merge(TransData,
                              on='transaction_id', how='left')
sales_data = sales_data.merge(DateData, on='date', how='left')

# Select the final columns for the sales_data DataFrame
sales_data = sales_data[['transaction_id','product_id',
                         'customer_id', 'quantity', 'date_id']]

# Save the final sales_data DataFrame to a CSV file
sales_data.to_csv(output_file_path, index=False)
```