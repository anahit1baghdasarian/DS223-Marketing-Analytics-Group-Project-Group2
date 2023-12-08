"""
Data Query Script

This script executes a series of SQL queries using the SqlHandler class to retrieve specific data
from a SQLite database. 
The queries cover various useful aspects for an analysis for an arbitrary company,
including customer, transactions, product, sales, and payment methods.

Queries:
1. Retrieve customers who made transactions in the month of January 2022.
2. Retrieve male customers from Singapore.
3. Retrieve products with prices greater than $50.
4. Retrieve transactions made using credit cards.
5. Calculate the total number of transactions grouped by month for the year 2022.
6. Retrieve product sales made in the year 2022.
7. Retrieve sales transactions done by customer with ID 5.
8. Retrieve products sold in the year 2022 with quantities greater than 10.
9. Count the number of products made in each country.
10. Retrieve the total number of transactions for each payment method.
11. Calculate the total sales amounts grouped by product category.
12. Calculate the average price of products bought by female customers.
13. Retrieve top 5 customers with the highest total sales amounts.
14. Retrieve products that were not involved in any sales transactions.
15. Retrieve the customer with the highest number of transactions in Spain.
16. Calculate total sales amounts grouped by quarter for the year 2010.
17. Retrieve products with prices less than the average price of all products.
18. Retrieve customers who made purchases in all quarters of the year 2023.
19. Retrieve the customers who made transactions using credit cards.
20. Retrieve the top 5 product producers with the highest total sales amounts.

Note: Each query is executed using the execute_custom_query method of the SqlHandler class.
"""

from CLV_Analysis.DB.sql_interactions import SqlHandler

Inst = SqlHandler('temp', ['sales_fact', 'transactions',
                           'customer', 'product', 'date'])

# Retrieve customers who made transactions in the month of January 2022.
query1 = """SELECT c.*
FROM customer c
JOIN transactions t
ON c.customer_id = t.customer_id
JOIN date d
ON t.date = d.date
WHERE d.year = 2022
AND d.month = 1;"""

# Retrieve male customers from Singapore.
query2 = """SELECT customer_id, customer_name, customer_surname
FROM customer
WHERE gender = 'Male'
AND country = 'Singapore';"""

# Retrieve products with prices greater than $50.
query3 = """SELECT *
FROM product
WHERE price > 50;"""

# Retrieve transactions made using credit cards.
query4 = """SELECT *
FROM transactions
WHERE payment_method = 'Credit Card';"""

# Calculate the total number of transactions
# grouped by month for the year 2022.
query5 = """SELECT d.month, COUNT(s.transaction_id)
AS transaction_count
FROM sales_fact s
JOIN date d
ON s.date_id = d.date_id
WHERE d.year = 2022
GROUP BY d.month;"""

# Retrieve product sales made in the year 2022.
query6 = """SELECT s.sales_id
FROM product p
JOIN sales_fact s
ON p.product_id = s.product_id
JOIN date d
ON s.date_id = d.date_id
WHERE d.year = 2022;"""

# Retrieve sales transactions done by customer with ID 5.
query7 = """SELECT *
FROM sales_fact
WHERE customer_id = 5;"""

# Retrieve products sold in the year 2022 with quantities greater than 10.
query8 = """SELECT p.*
FROM product p
JOIN sales_fact s
ON p.product_id = s.product_id
JOIN date d
ON s.date_id = d.date_id
WHERE d.year = 2022
AND s.quantity > 10;"""

# Count the number of product made in each country.
query9 = """SELECT producer_country, COUNT(*)
AS product_count
FROM product
GROUP BY producer_country;"""

# Retrieve the total number of transactions for each payment method.
query10 = """SELECT payment_method, COUNT(*)
AS transaction_count
FROM transactions
GROUP BY payment_method;"""

# Calculate the total sales amounts grouped by product category.
query11 = """SELECT p.product_category, SUM(s.quantity * p.price)
AS total_sales
FROM product p
LEFT JOIN sales_fact s
ON p.product_id = s.product_id
GROUP BY p.product_category;"""

# Calculate the average price of products bought by female customers.
query12 = """SELECT AVG(p.price)
AS average_price
FROM product p
JOIN sales_fact s
ON p.product_id = s.product_id
JOIN customer c
ON s.customer_id = c.customer_id
WHERE c.gender = 'Female';"""

# Retrieve top 5 customers with the highest total sales amounts.
query13 = """SELECT c.customer_name, c.customer_surname, SUM(s.quantity * p.price)
AS total_sales
FROM customer c
JOIN sales_fact s
ON c.customer_id = s.customer_id
JOIN product p
ON s.product_id = p.product_id
GROUP BY c.customer_id
ORDER BY total_sales DESC LIMIT 5;"""

# Retrieve products that were not involved in any sales transactions.
query14 = """SELECT p.*
FROM product p
LEFT JOIN sales_fact s
ON p.product_id = s.product_id
WHERE s.product_id IS NULL;"""

# Retrieve the customer with the highest number of transactions in Spain.
query15 = """SELECT c.customer_name, c.customer_surname, COUNT(s.transaction_id)
AS transaction_count
FROM customer c
JOIN sales_fact s
ON c.customer_id = s.customer_id
WHERE c.country = 'Spain'
GROUP BY c.customer_id
ORDER BY transaction_count DESC LIMIT 1;"""

# Calculate total sales amounts grouped by quarter for the year 2010.
query16 = """SELECT d.quarter, SUM(s.quantity*p.price)
AS total_sales_amount
FROM sales_fact s
JOIN date d
ON s.date_id = d.date_id
JOIN product p
ON s.product_id = p.product_id
WHERE d.year = 2010
GROUP BY d.quarter;"""

# Retrieve products with prices less than the average price of all products.
query17 = """SELECT *
FROM product
WHERE price < (SELECT AVG(price) FROM product);"""

# Retrieve customers who made purchases in all quarters of the year 2023.
query18 = """SELECT c.*
FROM customer c
WHERE NOT EXISTS (
    SELECT DISTINCT d.quarter
    FROM date d
    WHERE d.year = 2023
    EXCEPT
    SELECT DISTINCT d.quarter
    FROM date d
    JOIN sales_fact s ON d.date_id = s.date_id
    JOIN transactions t ON s.transaction_id = t.transaction_id
    WHERE t.customer_id = c.customer_id
);"""

# Retrieve the customers who made transactions using credit cards.
query19 = """SELECT c.*
FROM customer c
JOIN transactions t
ON c.customer_id = t.customer_id
WHERE t.payment_method = 'Credit Card';"""

# Retrieve the top 5 product producers with the highest total sales amounts.
query20 = """SELECT pr.producer_country, SUM(s.quantity * pr.price)
AS total_sales
FROM product pr
JOIN sales_fact s
ON pr.product_id = s.product_id
GROUP BY pr.producer_country
ORDER BY total_sales DESC LIMIT 5;"""


queries = [query1,
           query2,
           query3,
           query4,
           query5,
           query6,
           query7,
           query8,
           query9,
           query10,
           query11,
           query12,
           query13,
           query14,
           query15,
           query16,
           query17,
           query18,
           query19,
           query20]

for i in queries:
    Inst.execute_custom_query(i)
