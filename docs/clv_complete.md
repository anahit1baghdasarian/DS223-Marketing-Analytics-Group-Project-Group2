# **Complete Analysis with CLTVModel() Class**

## **Importing the Class and Making an Instance**

```py
from CLV_Analysis.Models.CLTV import CLTVModel
```

Instantiate the CLTVModel class
```py
cltv_model = CLTVModel()
```

Load data from the SQLite database
```py
cltv_model.load_data()
```

Check the loaded data
```py
cltv_model.check_data()
```

## **What is Customer Lifetime Value(CLV)?**

***The monetary value a customer will bring to a company during their relationship and communication is known as "customer lifetime value."***

This will be achieved by using the formulas below:

* **`Repeat rate`:** number of customers who make multiple purchases / all customers

* **`Churn rate`:** 1 - repeat rate

* **`Purchase frequency`:** total transactions / total number of unique customers

* **`Average order value`:** total price / total transactions

* **`Customer value`:** average order value * purchase frequency

* **`Profit margin`:** total price * profit margin rate(provided by the company)

* **`CLV`** = (customer value / churn rate) * profit margin

*Customers are segmented based on the generated CLV value, and operations are carried out according to these segments.*

#### **Default Dataset Details**

* **`sale_id`**: Unique Sale ID Number for each Respective Sale

* **`date`**: Date of Sales Transaction

* **`customer_id`**: Unique Customer iID for each Customer

* **`transaction_id`**: ID of the Transaction

* **`product_categor`y**: Product Category Name

* **`SKU`**: Product Code

* **`quantity`**: Number of Items Sold in the Transaction

* **`unit_price`** : Unit Price of the Respective Product

Calculate sales amount for each transaction
```py
cltv_model.calculate_sales_amount().head()
```

Calculate customer summary
```py
cltv_model.calculate_customer_summary().head()
```

Calculate average order value
```py
cltv_model.calculate_average_order_value().head()
```

Calculate purchase frequency
```py
cltv_model.calculate_purchase_frequency().head()
```

Calculate repeat rate
```py
cltv_model.calculate_repeat_rate()
```

Calculate churn rate
```py
cltv_model.calculate_churn_rate()
```

Calculate profit margin
```py
cltv_model.calculate_profit_margin().head()
```

Calculate customer value
```py
cltv_model.calculate_customer_value().head()
```

Calculate CLTV
```py
cltv_tb= cltv_model.calculate_cltv()
```

Create Segments
Divide the CLTV values into n parts and create a segment variable
```py
cltv_model.create_segments(customer_summary_pr=cltv_tb).head()
```

Display the summary of segments
```py
cltv_model.display_segments_summary(customer_summary_pr=cltv_tb)
```
## **CLV Prediction with BG-NBD and Gamma-Gamma**

**CLTV Prediction: BG/NBD Gamma gamma submodel**

Hereby, performing CLTV prediction with BG/NBD and Gamma-Gamma.

**Expected Number of Transactions with BG/NBD.**

BG/NBD is used as a standalone sales prediction model, that is; it predicts the expected number of purchases per customer.

**The information we need to use in this model and learn from the customer is:**

* **`frequency`:** Number of repeated purchases by the customer (more than 1) (frequency)

* **`recency`:** Time between a customer's first and last purchase

* **`T`:** Time since the customer's first purchase (customer's age)

Calculate CLTV prediction data
```py
cltv_model.calculate_cltv_pr().head()
```

Fit the BG-NBD model
```py
cltv_model.fit_bgf_model()
```

Plot frequency-recency matrix
```py
cltv_model.plot_frequency_recency_matrix()
```

Plot probability alive matrix
```py
cltv_model.plot_probability_alive_matrix()
```

### Ranking customers from best to worst

Let's return to our customers and rank them from "highest expected purchases in the next period" to lowest. Models expose a method that will predict a customer's expected purchases in the next period using their history.

Predict purchases
```py
cltv_model.predict_purchases().tail()
```

Plot period transactions
```py
cltv_model.plot_period_transactions()
```

### Estimating Customers' Lifetime Value
We can train our Gamma-Gamma submodel and predict the conditional, expected average lifetime value of our customers.

Fit the Gamma-Gamma model
```py
cltv_model.fit_ggf_model()
```

Calculate expected average profit
```py
cltv_model.calculate_expected_average_profit().head()
```

Calculate CLTV prediction for 3 months
```py
cltv_model.calculate_cltv_prediction(time_period = 3, discount_rate = 0.01/4).head()
```

Calculate CLTV prediction for 12 months
```py
cltv_model.calculate_cltv_prediction().head()
```

Merge CLTV predictions with other variables
```py
cltv_model.merge_cltv_predictions().head()
```

Create segments based on CLTV
```py
cltv_model.create_segments().head()
```

Display segments summary
```py
cltv_model.display_segments_summary()
```