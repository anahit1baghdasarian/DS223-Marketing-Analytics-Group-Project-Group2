# **The SqlHandler() and SQL Queries**

## **SQLite Database Handler Module**

The `CLV_Analysis/DB/sql_interactions` module defines the SqlHandler class, which handles SQLite database operations, including table manipulation and data import/export.

**Note:**

- This module assumes that the database connection is established
  using the SqlHandler class and follows a specific structure.

### **SqlHandler()**

#### Close the database connection.

```py
close_cnxn()
```
**Returns:** **`None`**

---------------------------------------------------------------

####  Retrieve column names of the specified table.

```py
get_table_columns()
```
**Returns:**

- **`list`**: List of column names.

---------------------------------------------------------------

#### Truncate the specified table.

```py
truncate_table()
```
**Returns:** **`None`**

---------------------------------------------------------------

#### Drop the specified table from the database.

This method executes an SQL query to drop the table specified by the `table_name` attribute.

```py
drop_table()
```
**Returns:** 

- **`None`**

**Raises:**

- **`Exception`:** If an error occurs while dropping the table.

**Note:**

- Ensure that the `table_name` attribute is properly set before calling this method.

- This operation is irreversible and permanently deletes the specified table.

---------------------------------------------------------------

#### Insert multiple rows into the specified table based on the given Pandas DataFrame.

```py
insert_many(df: pd.DataFrame)
```
**Returns:** 

- **`str`**

**Args:**

- **`df (pd.DataFrame)`**: Pandas DataFrame containing the data to be inserted.

**Raises:**

- **`Exception`**: If an error occurs while inserting the data into the table.

---------------------------------------------------------------

#### Retrieve data from the specified table in chunks and convert it into a Pandas DataFrame.

```py
from_sql_to_pandas(chunksize: int, id_value: str)
```

**Args:**

- **`chunksize (int)`**: Number of rows to fetch in each chunk.

- **`id_value (str)`**: Column name to be used for ordering and fetching data in chunks.

**Returns:**

- **`pd.DataFrame`**: Concatenated Pandas DataFrame containing the selected data.

---------------------------------------------------------------

#### Select a row from the specified table based on the given ID.

```py
select_by_id(id: int, db_name: str, table_name: str, table_id: str)
```

**Args:**

- **`id (int)`**: ID value to be used in the WHERE clause.

- **`db_name (str)`**: Name of the SQLite database.

- **`table_name (str)`**: Name of the table to be queried.

- **`table_id (str)`**: Name of the column representing the ID in the table.

**Returns:**

- **`dict`**: Dictionary containing the selected data.

---------------------------------------------------------------

#### Select multiple rows from the specified table based on the start ID and the number of rows.

```py
select_many(start_id: int, head: int, db_name: str, 
            table_name: str, table_id: str)
```
**Args:**

- **`start_id (int)`**: Starting ID value for the selection.

- **`head (int)`**: Number of rows to be retrieved.

- **`db_name (str)`**: Name of the SQLite database.

- **`table_name (str)`**: Name of the table to be queried.

- **`table_id (str)`**: Name of the column representing the ID in the table.

**Returns:**

- **`dict`**: Dictionary containing the selected data.

---------------------------------------------------------------

####  Delete a row from the specified table based on the given ID.

```py
delete_by_id(id: int, db_name: str, table_name: str, table_id: str)
```
**Args:**

- **`id (int)`**: ID value to be used in the WHERE clause.

- **`db_name (str)`**: Name of the SQLite database.

- **`table_name (str)`**: Name of the table to be deleted from.

- **`table_id (str)`**: Name of the column representing the ID in the table

---------------------------------------------------------------

#### Update a row in the specified table based on the given ID and update values.

```py
update_by_id(id: int, update_values: dict,
                     db_name: str, table_name: str, table_id: str)
```
**Args:**

**`id (int)`**: ID value to be used in the WHERE clause.

**`update_values (dict)`**: Dictionary containing column names as keys and new values as values.

**`db_name (str)`**: Name of the SQLite database.

**`table_name (str)`**: Name of the table to be updated.

**`table_id (str)`**: Name of the column representing the ID in the table.

--------------------------------------------------------------

#### Insert a new row into the specified table based on the given values.

```py
insert_by_id(insert_values: dict, db_name: str, table_name: str)
```
**Args:**

- **`insert_values (dict)`**: Dictionary containing column names as keys and values to be inserted as values.

- **`db_name (str)`**: Name of the SQLite database.

- **`table_name (str)`**: Name of the table to insert the new row into.

--------------------------------------------------------------

#### Execute a custom SQL query on the specified database connection.

```py
execute_custom_query(query, conn_string='temp.db')
```

**Args:**

- **`query (str)`**: SQL query to be executed.

- **`conn_string (str)`**: Database connection string (default is `temp.db`).

**Returns:**

- **`list`**: List of query results.

--------------------------------------------------------------

## **Queries to Test the Functionality of the Database**

### **Modules**

```py
from CLV_Analysis.DB.sql_interactions import SqlHandler
import pandas as pd
```
### **Create an Instance of SqlHandler() Class**

```py
Inst = SqlHandler('temp', ['sales_fact','transactions',
                           'customer','product', 'date'])
```

### **Write Some Queries**

```py
# Retrieve customers who made transactions in the month of January 2022.
query1 = """SELECT c.*
FROM customer c
JOIN transactions t
ON c.customer_id = t.customer_id
JOIN date d
ON t.date = d.date
WHERE d.year = 2022
AND d.month = 1;"""
```
```py
# Retrieve male customers from Singapore.
query2 = """SELECT customer_id, customer_name, customer_surname
FROM customer
WHERE gender = 'Male'
AND country = 'Singapore';"""
```
```py
# Retrieve products with prices greater than $50.
query3 = """SELECT *
FROM product
WHERE price > 50;"""
```
```py
queries = [query1,
           query2,
           query3]
```

### **Execute Queries**

```py
ls = []
for i in queries:
    ls.append(Inst.execute_custom_query(i))
```

### **Print the Results**

```py
count = 0

for i in ls:
    count+=1
    print(f'query {count}')
    print(pd.DataFrame(i))
    print("_______________")
```