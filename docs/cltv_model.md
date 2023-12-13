# **CLTVModel() Class**

The `CLTVModel` class is used for Customer Lifetime Value (CLTV) prediction based on the Beta Geo Fitter (`bgf`) and Gamma-Gamma Fitter (`ggf`) models from the lifetimes library.

**Note**:

- Ensure that the lifetimes, pandas, matplotlib, and warnings libraries are installed.

- The CLTVModel class assumes a specific structure in the loaded database and data.

-----------------------------------------

## Load data from the database.

```py 
load_data(query='''
        SELECT
            s.sales_id,
            d.date,
            s.customer_id,
            s.transaction_id,
            p.product_category,
            p.SKU,
            s.quantity,
            p.price as unit_price
        FROM
            date d 
        JOIN
            sales_fact s ON d.date_id = s.date_id
        JOIN
            product p ON s.product_id = p.product_id;
        ''')
```

**Parameters:**

- **`query (str)`**: SQL query to retrieve the data. Default is the provided query.

**Returns:**

- **`pd.DataFrame`**: Loaded DataFrame.

-----------------------------------------

## Display information about the DataFrame
**Including shape, info, unique values, missing values, quantiles, and head.**

```py
check_data(head=7, df = None)
```
**Parameters:**

- **`head (int)`:**  Number of rows to display. Default is 7.

- **df `(pd.DataFrame)`:**  DataFrame to check. Default is the `df` attribute.

**Returns:**

- `None`

-----------------------------------------

## Calculate and set the sales amount based on unit price and quantity.

```py
calculate_sales_amount(df = None,
                       unit_price_col= "unit_price",
                       quantity_col = 'quantity',
                       sales_amount_colname = "sales_amount")
```

**Parameters:**

- **`df (pd.DataFrame, optional)`**: DataFrame to perform calculations on. Default is the `df` attribute.

- **`unit_price_col (str, optional)`**: Column name of unit price. Default is `unit_price`.

- **`quantity_col (str, optional)`**: Column name of quantity. Default is `quantity`.

- **`sales_amount_colname (str, optional)`**: Column name for sales amount. Default is `sales_amount`.

**Returns:**

- **`pd.DataFrame`**: DataFrame with the sales amount column added.

-----------------------------------------

## Calculate and set customer summary metrics.
**Including total transactions and total sales amount.**

```py
calculate_customer_summary(df = None,
                           customer_id_col= 'customer_id',
                           transaction_id_col= 'transaction_id', 
                           sales_amount_col = None, 
                           total_transactions_colname = 'total_transactions',
                           total_sales_amount_colname = 'total_sales_amount')
```

**Parameters:**

- **`df (pd.DataFrame)`**: DataFrame to perform calculations on. Default is the `df` attribute.

- **`customer_id_col (str)`**: Column name of customer ID. Default is `customer_id`.

- **`transaction_id_col (str)`**: Column name of transaction ID. Default is `transaction_id`.

- **`sales_amount_col (pd.Series)`**: Series containing sales amount. Default is the `sales_amount` attribute.

- **`total_transactions_colname (str)`**: Column name for total transactions. Default is `total_transactions`.

- **`total_sales_amount_colname (str)`**: Column name for total sales amount. Default is `total_sales_amount`.

**Returns:**

- **`pd.DataFrame`**: Customer summary DataFrame with total transactions and total sales amount.

-----------------------------------------

## Calculate and set average order value.

```py
calculate_average_order_value(customer_summary = None,
                              total_sales_amount_col = None, 
                              total_transactions_col = None,
                              average_order_value_colname = 'average_order_value')
```
**Parameters:**

- **`customer_summary (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary` attribute.

- **`total_sales_amount_col (pd.Series, optional)`**: Series containing total sales amount. Default is the `total_sales_amount` attribute.

- **`total_transactions_col (pd.Series, optional)`**: Series containing total transactions. Default is the `total_transactions` attribute.

- **`average_order_value_colname (str, optional)`**: Column name for average order value. Default is `average_order_value`.

**Returns:**

- **`pd.DataFrame`**: Customer summary DataFrame with the average order value column added.

-----------------------------------------

## Calculate and set purchase frequency.

```py
calculate_purchase_frequency(customer_summary = None, 
                             total_transactions_col = None , 
                             purchase_frequency_colname = 'purchase_frequency')
```

**Parameters:**

- **`customer_summary (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary` attribute.

- **`total_transactions_col (pd.Series, optional)`**: Series containing total transactions. Default is the `total_transactions` attribute.

- **`purchase_frequency_colname (str, optional)`**: Column name for purchase frequency. Default is `purchase_frequency`.

**Returns:**

- **`pd.DataFrame`**: Customer summary DataFrame with the purchase frequency column added.

-----------------------------------------

## Calculate and set repeat rate.
```py
calculate_repeat_rate(customer_summary=None, total_transactions_col=None)
```
**Parameters:**

- **`customer_summary (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary`attribute.

- **`total_transactions_col (pd.Series, optional)`**: Series containing total transactions. Default is the `total_transactions` attribute.

**Returns:**

- **`float`**: Calculated repeat rate. Returns 0 if no customers with more than one transaction are found.

**Raises:**

- **`ValueError`**: If the required column is not present in the `customer_summary `DataFrame.

- **`Warning`**: If no customers with more than one transaction are found, a warning is raised.

**Notes:**

- The repeat rate is calculated as the ratio of customers with more than one transaction to the total number of customers.

-----------------------------------------

## Calculate and set churn rate.

```py
calculate_churn_rate(repeat_rate = None)
```
**Parameters:**

- **`repeat_rate (float)`**: Repeat rate of customers.Default is the `repeat_rate` attribute.

**Returns:**

- **`float`**: Calculated churn rate.

-----------------------------------------

## Calculate and set profit margin.

```py
calculate_profit_margin(profit_margin_rate=0.10,
                        customer_summary = None,
                        total_sales_amount_col = None,
                        profit_margin_colname = 'profit_margin')
```
**Parameters:**

- **`profit_margin_rate (float, optional)`**: Profit margin rate to be applied. Default is `0.10`.

- **`customer_summary (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary` attribute.

- **`total_sales_amount_col (pd.Series, optional)`**: Series containing total sales amount. Default is the `total_sales_amount` attribute.

- **`profit_margin_colname (str, optional)`**: Column name for profit margin. Default is `profit_margin`.

**Returns:**

- **`pd.DataFrame`**: Customer summary DataFrame with the profit margin column added.

**Raises:**

**`ValueError:`** If the required column is not present in the `customer_summary` DataFrame or if the DataFrame is empty.

**Notes:**

The profit margin is calculated by multiplying the total sales amount by the specified profit margin rate.

-----------------------------------------

## Calculate and set customer value.

```py
calculate_customer_value(customer_summary = None,
                         average_order_value_col = None,
                         purchase_frequency_col = None,
                         customer_value_colname = 'customer_value')
```

**Parameters:**

- **`customer_summary (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary` attribute.

- **`average_order_value_col (pd.Series, optional)`**: Series containing average order value. Default is the `average_order_value` attribute.

- **`purchase_frequency_col (pd.Series, optional)`**: Series containing purchase frequency. Default is the `purchase_frequency` attribute.

- **`customer_value_colname (str, optional)`**: Column name for customer value. Default is `customer_value`.

**Returns:**

- **`pd.DataFrame`**: Customer summary DataFrame with the customer value column added.

**Raises:**

**`ValueError`**: If the required columns are not present in the customer_summary DataFrame.

**Notes:**

Customer value is calculated as the product of average order value and purchase frequency.

-----------------------------------------

## Calculate and set customer lifetime value (CLTV).

```py
calculate_cltv(customer_summary = None ,
               churn_rate = None,
               customer_value_col = None, 
               profit_margin_col = None, 
               cltv_colname = 'clv')
```
**Parameters:**

- **`customer_summary (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary` attribute.

- **`churn_rate (float, optional)`**: Churn rate of customers. Default is the `churn_rate` attribute.

- **`customer_value_col (pd.Series, optional)`**: Series containing customer value. Default is the `customer_value` attribute.

- **`profit_margin_col (pd.Series, optional)`**: Series containing profit margin. Default is the `profit_margin` attribute.

- **`cltv_colname (str, optional)`**: Column name for CLTV. Default is `clv`.

**Returns:**

- **`pd.DataFrame`**: Customer summary DataFrame with the CLTV column added.

**Raises:**

**`ValueError`**: If the required columns are not present in the `customer_summary` DataFrame.

**Notes:**

CLTV is calculated as (Customer Value / Churn Rate) * Profit Margin.

-----------------------------------------

## Calculate and set customer lifetime value (CLTV) using the probabilistic model.

```py
calculate_cltv_pr(date_col = 'date', 
                  transaction_id_col = 'transaction_id',
                  customer_id_col = 'customer_id',
                  sales_amount_col = None,
                  df=None)
```

**Parameters:**

- **`date_col (str, optional)`**: Column name of date. Default is `date`.

- **`transaction_id_col (str, optional)`**: Column name of transaction ID. Default is `transaction_id`.

- **`customer_id_col (str, optional)`**: Column name of customer ID. Default is **customer_id**.

- **`sales_amount_col (pd.Series, optional)`**: Series containing sales amount. Default is the `sales_amount` attribute.

- **`df (pd.DataFrame, optional)`**: DataFrame to perform calculations on. Default is the `df` attribute.

**Returns:**

- **`None`**

**Raises:**

**`ValueError`**: If the required columns are not present in the DataFrame.

**Notes:**

CLTV is calculated using a probabilistic model based on recency, frequency, and monetary values.

-----------------------------------------

## Return column names for customer lifetime value (CLTV) using the probabilistic model.
**Used in calculate_cltv_pr()**

```py
_calculate_cltv_pr_columns(recency_colname = 'recency',
                           T_colname = 'T',
                           frequency_colname = 'frequency',
                           monetary_colname = 'monetary')
```

**Parameters:**

- **`recency_colname (str, optional)`**: Column name for recency. Default is `recency`.

- **`T_colname (str, optional)`**: Column name for T (age of the customer). Default is `T`.

- **`frequency_colname (str, optional)`**: Column name for frequency. Default is `frequency`.

- **`monetary_colname (str, optional)`**: Column name for monetary value. Default is `monetary`.

**Returns:**

- **`Tuple of str`**: Column names for recency, T, frequency, and monetary.

-----------------------------------------

## Secondary method used to calculate CLTV.
**Used in calculate_cltv_pr()**

```py
_calculate_recency_T(InvoiceDate)
```
**Parameters:**

**`InvoiceDate (pd.Series)`**: Series containing invoice dates.

**Returns:**

**`Tuple of int`**: Recency and T.

-----------------------------------------

## Secondary method used to calculate CLTV, considering a specific date.
**Used in calculate_cltv_pr()**

```py
_calculate_recency_today(InvoiceDate, df = None, date_col = 'date', days=1)
```
**Parameters:**

- **`InvoiceDate (pd.Series)`**: Series containing invoice dates.

- **`df (pd.DataFrame, optional)`**: DataFrame to retrieve the maximum date. Default is the `df` attribute.

- **`date_col (str, optional)`**: Column name of date. Default is `date`.

- **`days (int, optional)`**: Number of days to consider for recency. Default is 1.

**Returns:**

- **`int:`** Recency considering today's date.

-----------------------------------------

## Calculate and set monetary value, frequency, recency, and T after applying filters.
**Used in calculate_cltv_pr()**

```py
_calculate_monetary_frequency_filter(customer_summary_pr=None,
                                     monetary_col=None,
                                     frequency_col=None,
                                     recency_col=None, T_col=None)
```

**Parameters:**

- **`customer_summary_pr (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary_pr` attribute.

- **`monetary_col (pd.Series, optional)`**: Series containing monetary value. Default is the `monetary` attribute.

- **`frequency_col (pd.Series, optional)`**: Series containing frequency. Default is the `frequency` attribute.

- **`recency_col (pd.Series, optional)`**: Series containing recency. Default is the `recency` attribute.

- **`T_col (pd.Series, optional)`**: Series containing T (age of the customer). Default is the `T` attribute.

**Returns:**

**`None`**

**Raises:**

**`ValueError`**: If the required columns are not present in the `customer_summary_pr` DataFrame.

-----------------------------------------

## Fit the Beta Geo Fitter (BG/NBD) model using the provided frequency, recency, and T values.

```py
fit_bgf_model(customer_summary_pr = None,
              frequency_colname = "frequency",
              recency_colname = "recency",
              T_colname = "T")
```

**Parameters:**

- **`customer_summary_pr (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary_pr` attribute.

- **`frequency_colname (str, optional)`**: Column name of the customer transaction frequency. Default is `frequency`.

- **`recency_colname (str, optional)`**: Column name of the recency (time since the last transaction). Default is `recency`.

- **`T_colname (str, optional)`**: Column name of the T (age of the customer). Default is `T`.

**Returns:**

**`None`**

-----------------------------------------

## Plot the frequency-recency matrix using the fitted BG/NBD model.

```py
plot_frequency_recency_matrix(BetaGeoFitter = None)
```
**Parameters:**

- **`BetaGeoFitter (lifetimes.BetaGeoFitter, optional)`**: An instance of the BetaGeoFitter model. If not provided, the internal BetaGeoFitter instance associated with the CLTVModel will be used.

**Returns:**

**`None`**

-----------------------------------------

## Plot the probability alive matrix using the fitted BG/NBD model.

```py
plot_probability_alive_matrix(BetaGeoFitter = None)
```
**Parameters:**

- **`BetaGeoFitter (lifetimes.BetaGeoFitter, optional)`**: An instance of the BetaGeoFitter model. If not provided, the internal BetaGeoFitter instance associated with the CLTVModel will be used.

**Returns:**

**`None`**

-----------------------------------------

## Predict the number of purchases a customer will make in the future.

```py
predict_purchases(t=1, customer_summary_pr=None,
                  frequency_col=None,
                  recency_col=None, 
                  T_col=None,
                  predicted_purchases_colname='predicted_purchases')
```
**Parameters:**

- **`t (int, optional)`**: Time period for future predictions. Default is 1.

- **`customer_summary_pr (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary_pr` attribute.

- **`frequency_col (pd.Series, optional)`**: Series containing customer transaction frequency. Default is the `frequency` attribute.

- **`recency_col (pd.Series, optional)`**: Series containing recency (time since the last transaction). Default is the `recency` attribute.

- **`T_col (pd.Series, optional)`**: Series containing T (age of the customer). Default is the `T` attribute.

- **`predicted_purchases_colname (str, optional)`**: Column name for predicted purchases. Default is `predicted_purchases`.

Returns:

- **`pd.DataFrame`**: Customer summary DataFrame sorted by predicted purchases.

-----------------------------------------

## Plot the actual and predicted number of transactions in each time period.

```py
plot_period_transactions(BetaGeoFitter = None)
```

**Parameters:**

- **`BetaGeoFitter (lifetimes.BetaGeoFitter, optional)`**: An instance of the BetaGeoFitter model. If not provided, the internal BetaGeoFitter instance associated with the CLTVModel will be used.

**Returns:**

**`None`**

-----------------------------------------

## Fit the Gamma-Gamma Fitter (GGF) model using the provided frequency and monetary values.

```py
fit_ggf_model(customer_summary_pr=None,
              frequency_colname="frequency",
              monetary_colname="monetary")
```

**Parameters:**

- **`customer_summary_pr (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is `the customer_summary_pr` attribute.

- **`frequency_colname (str, optional)`**: Column name of customer transaction frequency. Default is `frequency`.

- **`monetary_colname (str, optional)`**: Column name of customer monetary value. Default is `monetary`.

**Returns:**

**`None`**

-----------------------------------------

## Calculate the expected average profit per transaction.

```py
calculate_expected_average_profit(customer_summary_pr = None, 
                                  frequency_colname="frequency", 
                                  monetary_colname="monetary",
                                  exp_avg_profit_colname = "expected_average_profit")
```

**Parameters:**

- **`customer_summary_pr (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary_pr` attribute.

- **`frequency_colname (str, optional)`**: Column name for customer transaction frequency. Default is `frequency`.

- **`monetary_colname (str, optional)`**: Column name of customer monetary value. Default is `monetary`.

- **`exp_avg_profit_colname (str, optional)`**: Column name for expected average profit. Default is `expected_average_profit`.

**Returns:**

- **`pd.DataFrame`**: Customer summary DataFrame sorted by expected average profit (descending).

-----------------------------------------

## Calculate Customer Lifetime Value (CLTV) predictions using the fitted models.

```py
calculate_cltv_prediction(time_period=12,
                          discount_rate=0.01,
                          freq="W",
                          frequency_col=None,
                          recency_col=None,
                          T_col=None,
                          monetary_col=None)
```

**Parameters:**

- **`time_period (int, optional)`**: Time period for CLTV predictions. Default is 12.

- **`discount_rate (float, optional)`**: Discount rate for future cash flows. Default is 0.01.

- **`freq (str, optional)`**: Frequency of time periods. Default is `W` (weekly).
{“D”, “H”, “M”, “W”} for day, hour, month, week.

- **`frequency_col (pd.Series, optional)`**: Series containing customer transaction frequency. Default is the `frequency` attribute.

- **`recency_col (pd.Series, optional)`**: Series containing recency (time since the last transaction). Default is the `recency` attribute.

- **`T_col (pd.Series, optional)`**: Series containing T (age of the customer). Default is the `T` attribute.

- **`monetary_col (pd.Series, optional)`**: Series containing customer monetary value. Default is the `monetary` attribute.

**Returns:**

**`pd.DataFrame`**: CLTV predictions for each customer.

-----------------------------------------

## Merge CLTV predictions with the original DataFrame.

```py
merge_cltv_predictions(cltv_pred = None,
                       customer_summary_pr = None,
                       df = None,
                       customer_id_col = "customer_id",
                       how = 'left')
```

**Parameters:**

- **`cltv_pred (pd.DataFrame, optional)`**: CLTV predictions DataFrame. Default is the `cltv_pred` attribute.

- **`customer_summary_pr (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary_pr` attribute.

- **`df (pd.DataFrame, optional)`**: Original DataFrame containing customer data. Default is the `df` attribute.

- **`customer_id_col (str, optional)`**: Column name of customer ID. Default is `customer_id`.

- **`how (str, optional)`**: Type of merge to be performed (e.g., 'left', 'right', 'outer', 'inner'). Default is `left`.

**Returns:**

**`None`**

-----------------------------------------

## Create customer segments based on CLTV predictions.

```py
create_segments(customer_summary_pr = None,
                clv_col = 'clv',
                segment_colname = 'segment',
                num_segments = 4,
                labels = ["D", "C", "B", "A"])
```

**Parameters:**

- **`customer_summary_pr (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary_pr` attribute.

- **`clv_col (str, optional)`**: Column name for Customer Lifetime Value (CLV). Default is `clv`.

- **`segment_colname (str, optional)`**: Column name for the created segment. Default is `segment`.

- **`num_segments (int, optional)`**: Number of segments to create. Default is 4.

- **`labels (list, optional)`**: Labels for the created segments. Default is `["D", "C", "B", "A"]`.

**Returns:**

**`None`**

-----------------------------------------

## Display a summary of customer segments, including count, mean, and sum.

```py
display_segments_summary(segment_col = None, customer_summary_pr = None)
```

**Parameters:**

- **`segment_col (pd.Series, optional)`**: Series containing customer segments. Default is the `segment` attribute.

- **`customer_summary_pr (pd.DataFrame, optional)`**: Customer summary DataFrame. Default is the `customer_summary_pr` attribute.

**Returns:**

- **`pd.DataFrame`**: Summary statistics for each customer segment.

-----------------------------------------