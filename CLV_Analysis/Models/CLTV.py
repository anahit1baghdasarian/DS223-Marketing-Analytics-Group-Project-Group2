"""
CLTV Model Module

This module defines the `CLTVModel` class, which is used for Customer Lifetime Value (CLTV) prediction
based on the Beta Geo Fitter (bgf) and Gamma-Gamma Fitter (ggf) models from the lifetimes library.

Classes:
- CLTVModel: Customer Lifetime Value (CLTV) Model class.

Note:
- Ensure that the lifetimes, pandas, matplotlib, and warnings libraries are installed.
- The CLTVModel class assumes a specific structure in the loaded database and data.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from lifetimes.plotting import plot_frequency_recency_matrix, plot_probability_alive_matrix, plot_period_transactions
from lifetimes import BetaGeoFitter, GammaGammaFitter
import warnings

class CLTVModel:
    """
    Customer Lifetime Value (CLTV) Model class that calculates and predicts customer lifetime value.
    The class uses the Beta Geo Fitter (bgf) and Gamma-Gamma Fitter (ggf) models from lifetimes library.

    Parameters:
        database_path (str): Path to the SQLite database file. Default is 'data.db'.

    Attributes:
        conn (sqlite3.Connection): SQLite database connection.
        df (pd.DataFrame): DataFrame containing sales data.
        sales_amount (pd.Series): Series containing sales amount.
        customer_summary (pd.DataFrame): DataFrame summarizing customer transactions.
        customer_summary_pr (pd.DataFrame): DataFrame for customer predictions.
        repeat_rate (float): Repeat rate of customers.
        total_transactions (pd.Series): Series containing total transactions per customer.
        total_sales_amount (pd.Series): Series containing total sales amount per customer.
        purchase_frequency (pd.Series): Series containing purchase frequency per customer.
        average_order_value (pd.Series): Series containing average order value per customer.
        churn_rate (float): Churn rate of customers.
        profit_margin (pd.Series): Series containing profit margin per customer.
        customer_value (pd.Series): Series containing customer value.
        cltv (pd.Series): Series containing CLTV per customer.
        recency (pd.Series): Series containing recency values for CLTV prediction.
        T (pd.Series): Series containing T values for CLTV prediction.
        frequency (pd.Series): Series containing frequency values for CLTV prediction.
        monetary (pd.Series): Series containing monetary values for CLTV prediction.
        cltv_pred (pd.DataFrame): DataFrame containing CLTV predictions.
        predicted_purchases (pd.Series): Series containing predicted purchases per customer.
        segment (pd.Series): Series containing customer segments.
        bgf (lifetimes.BetaGeoFitter): Beta Geo Fitter model.
        ggf (lifetimes.GammaGammaFitter): Gamma-Gamma Fitter model.
    """

    def __init__(self, database_path='data.db'):
        """
        Initialize the CLTVModel object.

        Parameters:
            database_path (str): Path to the SQLite database file. Default is 'data.db'.
        """
        self.conn = sqlite3.connect(database_path)
        self.df = None
        self.sales_amount = None
        self.customer_summary = None  
        self.customer_summary_pr = None
        self.repeat_rate = None
        self.total_transactions = None
        self.total_sales_amount = None
        self.purchase_frequency = None
        self.average_order_value = None
        self.churn_rate = None
        self.profit_margin = None
        self.customer_value =  None
        self.cltv = None
        self.recency = None
        self.T = None
        self.frequency = None
        self.monetary = None
        self.cltv_pred = None
        self.predicted_purchases = None
        self.segment = None
        self.bgf = BetaGeoFitter(penalizer_coef=0.001)
        self.ggf = GammaGammaFitter(penalizer_coef=0.01)

    def load_data(self, query='''
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
        '''):
        """
        Load data from the database and set it as the DataFrame 'df'.

        Parameters:
            query (str): SQL query to retrieve the data. Default is the provided query.

        Returns:
            pd.DataFrame: Loaded DataFrame.
        """
        self.df = pd.read_sql_query(query, self.conn)
        return self.df

    def check_data(self, head=7, df = None):
        """
        Display information about the DataFrame, including shape, info, unique values, missing values, quantiles, and head.

        Parameters:
            head (int): Number of rows to display. Default is 7.
            df (pd.DataFrame): DataFrame to check. Default is the 'df' attribute.

        Returns:
            None
        """
        if df is None:
            df = self.df
        print("################### Shape ####################")
        print(df.shape)
        print("#################### Info #####################")
        print(df.info())
        print("################### Nunique ###################")
        print(df.nunique())
        print("##################### NA #####################")
        print(df.isnull().sum())
        print("################## Quantiles #################")
        print(df.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)
        print("#################### Head ####################")
        print(df.head(head))

    def calculate_sales_amount(self, df = None, unit_price_col= "unit_price", quantity_col = 'quantity', sales_amount_colname = "sales_amount"):
        """
        Calculate and set the sales amount based on unit price and quantity.

        Parameters:
            - df (pd.DataFrame, optional): DataFrame to perform calculations on. Default is the 'df' attribute.
            - unit_price_col (str, optional): Column name for unit price. Default is 'unit_price'.
            - quantity_col (str, optional): Column name for quantity. Default is 'quantity'.
            - sales_amount_colname (str, optional): Column name for sales amount. Default is 'sales_amount'.

        Returns:
            pd.DataFrame: DataFrame with the sales amount column added.
        """
        if df is None:
            df = self.df
        if unit_price_col not in df.columns:
            raise ValueError(f"The {unit_price_col} column is required in {df}.")
        if quantity_col not in df.columns:
            raise ValueError(f"The {quantity_col} column is required in {df}.")
 
        df[sales_amount_colname] = df[unit_price_col] * df[quantity_col]
        self.sales_amount = df[sales_amount_colname]
        return df

    def calculate_customer_summary(self, df = None, customer_id_col= 'customer_id',
                                   transaction_id_col= 'transaction_id', sales_amount_col = None, 
                                   total_transactions_colname = 'total_transactions', total_sales_amount_colname = 'total_sales_amount'):
        """
        Calculate and set customer summary metrics, including total transactions and total sales amount.

        Parameters:
            df (pd.DataFrame): DataFrame to perform calculations on. Default is the 'df' attribute.
            customer_id_col (str): Column name for customer ID. Default is 'customer_id'.
            transaction_id_col (str): Column name for transaction ID. Default is 'transaction_id'.
            sales_amount_col (pd.Series): Series containing sales amount. Default is the 'sales_amount' attribute.
            total_transactions_colname (str): Column name for total transactions. Default is 'total_transactions'.
            total_sales_amount_colname (str): Column name for total sales amount. Default is 'total_sales_amount'.

        Returns:
            pd.DataFrame: Customer summary DataFrame with total transactions and total sales amount.
        """
        if df is None:
            df = self.df
        if customer_id_col not in df.columns:
            raise ValueError(f"The {customer_id_col} column is required in {df}.")
        if transaction_id_col not in df.columns:
            raise ValueError(f"The {transaction_id_col} column is required in {df}.")
        if sales_amount_col is None:
            sales_amount_col = self.sales_amount
        if sales_amount_col.name not in df.columns:
            raise ValueError(f"The {sales_amount_col.name} column is required in {df}.")
            
        self.customer_summary = df.groupby(customer_id_col).agg({
            transaction_id_col: lambda x: x.nunique(),
            sales_amount_col.name: lambda x: x.sum()
        })
        self.customer_summary.columns = [total_transactions_colname, total_sales_amount_colname]
        self.total_transactions = self.customer_summary[total_transactions_colname]
        self.total_sales_amount = self.customer_summary[total_sales_amount_colname]
        return self.customer_summary
    
    def calculate_average_order_value(self, customer_summary = None,
                                      total_sales_amount_col = None, total_transactions_col = None,
                                      average_order_value_colname = 'average_order_value'):
        """
        Calculate and set average order value.

        Parameters:
            - customer_summary (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary' attribute.
            - total_sales_amount_col (pd.Series, optional): Series containing total sales amount. Default is the 'total_sales_amount' attribute.
            - total_transactions_col (pd.Series, optional): Series containing total transactions. Default is the 'total_transactions' attribute.
            - average_order_value_colname (str, optional): Column name for average order value. Default is 'average_order_value'.

        Returns:
            pd.DataFrame: Customer summary DataFrame with the average order value column added.
        """
        if customer_summary is None:
            customer_summary = self.customer_summary
        if total_sales_amount_col is None:
            total_sales_amount_col = self.total_sales_amount
        if total_sales_amount_col.name not in customer_summary.columns:
            raise ValueError(f"The {total_sales_amount_col.name} column is required in {customer_summary}.")
        if total_transactions_col is None:
            total_transactions_col = self.total_transactions
        if total_transactions_col.name not in customer_summary.columns:
            raise ValueError(f"The {total_transactions_col.name} column is required in {customer_summary}.")
        
        customer_summary[average_order_value_colname] = total_sales_amount_col/ total_transactions_col
        self.average_order_value = customer_summary[average_order_value_colname]
        return customer_summary

    def calculate_purchase_frequency(self, customer_summary = None, 
                                     total_transactions_col = None , purchase_frequency_colname = 'purchase_frequency'):
        """
        Calculate and set purchase frequency.

        Parameters:
            - customer_summary (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary' attribute.
            - total_transactions_col (pd.Series, optional): Series containing total transactions. Default is the 'total_transactions' attribute.
            - purchase_frequency_colname (str, optional): Column name for purchase frequency. Default is 'purchase_frequency'.

        Returns:
            pd.DataFrame: Customer summary DataFrame with the purchase frequency column added.
        """
        if customer_summary is None:
            customer_summary = self.customer_summary
        if total_transactions_col is None:
            total_transactions_col = self.total_transactions
        if total_transactions_col.name not in customer_summary.columns:
            raise ValueError(f"The {total_transactions_col.name} column is required in {customer_summary}.")
        if customer_summary.shape[0] == 0:
            raise ValueError(f"The {customer_summary} DataFrame is empty.")
    
        customer_summary[purchase_frequency_colname] = total_transactions_col / customer_summary.shape[0]
        self.purchase_frequency = customer_summary[purchase_frequency_colname]
        return customer_summary
    
    def calculate_repeat_rate(self, customer_summary=None, total_transactions_col=None):
        """
        Calculate and set repeat rate.

        Parameters:
            - customer_summary (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary' attribute.
            - total_transactions_col (pd.Series, optional): Series containing total transactions. Default is the 'total_transactions' attribute.

        Returns:
            float: Calculated repeat rate. Returns 0 if no customers with more than one transaction are found.

        Raises:
            ValueError: If the required column is not present in the customer_summary DataFrame.
            Warning: If no customers with more than one transaction are found, a warning is raised.

        Notes:
            The repeat rate is calculated as the ratio of customers with more than one transaction to the total number of customers.
        """
        if customer_summary is None:
            customer_summary = self.customer_summary

        if total_transactions_col is None:
            total_transactions_col = self.total_transactions

        if total_transactions_col.name not in customer_summary.columns:
            raise ValueError(f"The {total_transactions_col.name} column is required in {customer_summary}.")

        if len(customer_summary) == 0:
            raise ValueError(f"The {customer_summary} DataFrame is empty.")

        repeat_rate_df = customer_summary[total_transactions_col > 1]

        if len(repeat_rate_df) == 0:
            warnings.warn("No customers with more than one transaction found. Repeat rate will be 0.", Warning)
            self.repeat_rate = 0
            return self.repeat_rate
        else:
            repeat_rate = len(repeat_rate_df) / len(customer_summary)
            self.repeat_rate = repeat_rate
            return repeat_rate

    def calculate_churn_rate(self, repeat_rate = None):
        """
        Calculate and set churn rate.

        Parameters:
            repeat_rate (float): Repeat rate of customers. 
                Default is the 'repeat_rate' attribute.

        Returns:
            float: Calculated churn rate.
        """
        if repeat_rate is None:
            repeat_rate = self.repeat_rate
        churn_rate = 1 - repeat_rate
        self.churn_rate = churn_rate
        return churn_rate

    def calculate_profit_margin(self, profit_margin_rate=0.10,
                                customer_summary = None, total_sales_amount_col = None,
                                profit_margin_colname = 'profit_margin'):
        """
        Calculate and set profit margin.

        Parameters:
            - profit_margin_rate (float, optional): Profit margin rate to be applied. Default is 0.10.
            - customer_summary (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary' attribute.
            - total_sales_amount_col (pd.Series, optional): Series containing total sales amount. Default is the 'total_sales_amount' attribute.
            - profit_margin_colname (str, optional): Column name for profit margin. Default is 'profit_margin'.

        Returns:
            pd.DataFrame: Customer summary DataFrame with the profit margin column added.

        Raises:
            ValueError: If the required column is not present in the customer_summary DataFrame or if the DataFrame is empty.

        Notes:
            The profit margin is calculated by multiplying the total sales amount by the specified profit margin rate.
        """
        if customer_summary is None:
            customer_summary = self.customer_summary

        if len(customer_summary) == 0:
            raise ValueError(f"The {customer_summary} DataFrame is empty.")

        if total_sales_amount_col is None:
            total_sales_amount_col = self.total_sales_amount

        if total_sales_amount_col.name not in customer_summary.columns:
            raise ValueError(f"The {total_sales_amount_col.name} column is required in {customer_summary}.")

        customer_summary[profit_margin_colname] = total_sales_amount_col * profit_margin_rate
        self.profit_margin = customer_summary[profit_margin_colname]
        return customer_summary

    def calculate_customer_value(self, customer_summary = None, average_order_value_col = None, purchase_frequency_col = None,
                                 customer_value_colname = 'customer_value'):
        """
        Calculate and set customer value.

        Parameters:
            - customer_summary (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary' attribute.
            - average_order_value_col (pd.Series, optional): Series containing average order value. Default is the 'average_order_value' attribute.
            - purchase_frequency_col (pd.Series, optional): Series containing purchase frequency. Default is the 'purchase_frequency' attribute.
            - customer_value_colname (str, optional): Column name for customer value. Default is 'customer_value'.

        Returns:
            pd.DataFrame: Customer summary DataFrame with the customer value column added.

        Raises:
            ValueError: If the required columns are not present in the customer_summary DataFrame.

        Notes:
            Customer value is calculated as the product of average order value and purchase frequency.
        """
        if customer_summary is None:
            customer_summary = self.customer_summary
        if average_order_value_col is None:
            average_order_value_col = self.average_order_value
        if average_order_value_col.name not in customer_summary.columns:
            raise ValueError(f"The {average_order_value_col.name} column is required in {customer_summary}.")
        if purchase_frequency_col is None:
            purchase_frequency_col = self.purchase_frequency
        if purchase_frequency_col.name not in customer_summary.columns:
            raise ValueError(f"The {purchase_frequency_col.name} column is required in {customer_summary}.")
        customer_summary[customer_value_colname] = average_order_value_col * purchase_frequency_col
        self.customer_value = customer_summary[customer_value_colname]
        return customer_summary

    def calculate_cltv(self, customer_summary = None ,churn_rate = None, customer_value_col = None, 
                       profit_margin_col = None, cltv_colname = 'clv'):
        """
        Calculate and set customer lifetime value (CLTV).

        Parameters:
            - customer_summary (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary' attribute.
            - churn_rate (float, optional): Churn rate of customers. Default is the 'churn_rate' attribute.
            - customer_value_col (pd.Series, optional): Series containing customer value. Default is the 'customer_value' attribute.
            - profit_margin_col (pd.Series, optional): Series containing profit margin. Default is the 'profit_margin' attribute.
            - cltv_colname (str, optional): Column name for CLTV. Default is 'cltv'.

        Returns:
            pd.DataFrame: Customer summary DataFrame with the CLTV column added.

        Raises:
            ValueError: If the required columns are not present in the customer_summary DataFrame.

        Notes:
            CLTV is calculated as (Customer Value / Churn Rate) * Profit Margin.
        """
        if customer_summary is None:
            customer_summary = self.customer_summary
        if churn_rate is None:
            churn_rate = self.churn_rate
        if customer_value_col is None:
            customer_value_col = self.customer_value
        if customer_value_col.name not in customer_summary.columns:
            raise ValueError(f"The {customer_value_col.name} column is required in {customer_summary}.")
        if profit_margin_col is None:
            profit_margin_col = self.profit_margin
        if profit_margin_col.name not in customer_summary.columns:
            raise ValueError(f"The {profit_margin_col.name} column is required in {customer_summary}.")
        
        customer_summary[cltv_colname] = (customer_value_col / churn_rate) * profit_margin_col
        self.cltv = customer_summary[cltv_colname]
        return customer_summary

    def calculate_cltv_pr(self, date_col = 'date', transaction_id_col = 'transaction_id', customer_id_col = 'customer_id', sales_amount_col = None, df=None):
        """
        Calculate and set customer lifetime value (CLTV) using the probabilistic model.

        Parameters:
            - date_col (str, optional): Column name for date. Default is 'date'.
            - transaction_id_col (str, optional): Column name for transaction ID. Default is 'transaction_id'.
            - customer_id_col (str, optional): Column name for customer ID. Default is 'customer_id'.
            - sales_amount_col (pd.Series, optional): Series containing sales amount. Default is the 'sales_amount' attribute.
            - df (pd.DataFrame, optional): DataFrame to perform calculations on. Default is the 'df' attribute.

        Returns:
            None

        Raises:
            ValueError: If the required columns are not present in the DataFrame.

        Notes:
            CLTV is calculated using a probabilistic model based on recency, frequency, and monetary values.
        """
        if df is None:
            df = self.df
        if sales_amount_col is None:
            sales_amount_col = self.sales_amount
        if sales_amount_col.name not in df.columns:
            raise ValueError(f"The {sales_amount_col.name} column is required in {df}.")
        if date_col not in df.columns:
            raise ValueError(f"The {date_col} column is required in {df}.")
        if transaction_id_col not in df.columns:
            raise ValueError(f"The {transaction_id_col} column is required in {df}.")
        if customer_id_col not in df.columns:
            raise ValueError(f"The {customer_id_col} column is required in {df}.")

        recency_col, T_col, frequency_col, monetary_col = self._calculate_cltv_pr_columns()

        customer_summary_pr = df.groupby(customer_id_col).agg({
            date_col: [lambda InvoiceDate: self._calculate_recency_T(InvoiceDate),
                          lambda InvoiceDate: self._calculate_recency_today(InvoiceDate)],
            transaction_id_col: lambda Invoice: Invoice.nunique(),
            sales_amount_col.name: lambda TotalPrice: TotalPrice.sum()
        })

        customer_summary_pr.columns = customer_summary_pr.columns.droplevel(0)
        customer_summary_pr.columns = [recency_col, T_col, frequency_col, monetary_col]
        self.recency = customer_summary_pr[recency_col]
        self.T = customer_summary_pr[T_col]
        self.frequency = customer_summary_pr[frequency_col]
        self.monetary = customer_summary_pr[monetary_col]

        self.customer_summary_pr = customer_summary_pr
        self._calculate_monetary_frequency_filter()
        return customer_summary_pr

    def _calculate_cltv_pr_columns(self, recency_colname = 'recency', T_colname = 'T',
                                   frequency_colname = 'frequency', monetary_colname = 'monetary'):
       """
        Calculate and return column names for customer lifetime value (CLTV) using the probabilistic model.

        Parameters:
            - recency_colname (str, optional): Column name for recency. Default is 'recency'.
            - T_colname (str, optional): Column name for T (age of the customer). Default is 'T'.
            - frequency_colname (str, optional): Column name for frequency. Default is 'frequency'.
            - monetary_colname (str, optional): Column name for monetary value. Default is 'monetary'.

        Returns:
            Tuple of str: Column names for recency, T, frequency, and monetary.
        """
       return recency_colname, T_colname, frequency_colname, monetary_colname


    def _calculate_recency_T(self, InvoiceDate):
        """
        Calculate recency and T (age of the customer) based on the given InvoiceDate.

        Parameters:
            InvoiceDate (pd.Series): Series containing invoice dates.

        Returns:
            Tuple of int: Recency and T.
        """
        InvoiceDate = pd.to_datetime(InvoiceDate)
        return (InvoiceDate.max() - InvoiceDate.min()).days

    def _calculate_recency_today(self, InvoiceDate, df = None, date_col = 'date', days=1):
        """
        Calculate recency considering today's date based on the given InvoiceDate.

        Parameters:
            - InvoiceDate (pd.Series): Series containing invoice dates.
            - df (pd.DataFrame, optional): DataFrame to retrieve the maximum date. Default is the 'df' attribute.
            - date_col (str, optional): Column name for date. Default is 'date'.
            - days (int, optional): Number of days to consider for recency. Default is 1.

        Returns:
            int: Recency considering today's date.

        Notes:
            The default value for the 'days' parameter is 1.
        """
        if df is None:
            df = self.df
        InvoiceDate = pd.to_datetime(InvoiceDate)
        max_date = pd.to_datetime(df[date_col].max())
        today = max_date + pd.Timedelta(days=days)
        return (today - InvoiceDate.min()).days

    def _calculate_monetary_frequency_filter(self, customer_summary_pr=None, monetary_col=None, frequency_col=None,
                                         recency_col=None, T_col=None):
        """
        Calculate and set monetary value, frequency, recency, and T after applying filters.

        Parameters:
            - customer_summary_pr (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary_pr' attribute.
            - monetary_col (pd.Series, optional): Series containing monetary value. Default is the 'monetary' attribute.
            - frequency_col (pd.Series, optional): Series containing frequency. Default is the 'frequency' attribute.
            - recency_col (pd.Series, optional): Series containing recency. Default is the 'recency' attribute.
            - T_col (pd.Series, optional): Series containing T (age of the customer). Default is the 'T' attribute.

        Returns:
            None

        Raises:
            ValueError: If the required columns are not present in the customer_summary_pr DataFrame.
        """
        if customer_summary_pr is None:
            customer_summary_pr = self.customer_summary_pr
        if monetary_col is None:
            monetary_col = self.monetary
        if monetary_col.name not in customer_summary_pr.columns:
            raise ValueError(f"The {monetary_col.name} column is required in {customer_summary_pr}.")
        if frequency_col is None:
            frequency_col = self.frequency
        if frequency_col.name not in customer_summary_pr.columns:
            raise ValueError(f"The {frequency_col.name} column is required in {customer_summary_pr}.")
        if recency_col is None:
            recency_col = self.recency
        if recency_col.name not in customer_summary_pr.columns:
            raise ValueError(f"The {recency_col.name} column is required in {customer_summary_pr}.")
        if T_col is None:
            T_col = self.T
        if T_col.name not in customer_summary_pr.columns:
            raise ValueError(f"The {T_col.name} column is required in {customer_summary_pr}.")

        self.monetary = monetary_col / frequency_col
        customer_summary_pr[monetary_col.name] = self.monetary

        customer_summary_pr = customer_summary_pr[frequency_col > 1]
        self.frequency = customer_summary_pr[frequency_col.name]

        self.recency = recency_col / 7
        customer_summary_pr[recency_col.name] = self.recency

        self.T = T_col / 7
        customer_summary_pr[T_col.name] = self.T

        self.customer_summary_pr = customer_summary_pr

    def fit_bgf_model(self, customer_summary_pr = None, frequency_colname = "frequency",
                      recency_colname = "recency", T_colname = "T"):
        """
        Fit the Beta Geo Fitter (BG/NBD) model using the provided frequency, recency, and T values.

        Parameters:
            - customer_summary_pr (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary_pr' attribute.
            - frequency_colname (str, optional): Column name for customer transaction frequency. Default is 'frequency'.
            - recency_colname (str, optional): Column name for recency (time since the last transaction). Default is 'recency'.
            - T_colname (str, optional): Column name for T (age of the customer). Default is 'T'.

        Returns:
            None
        """
        if customer_summary_pr is None:
            customer_summary_pr = self.customer_summary_pr
        
        frequency_col = customer_summary_pr[frequency_colname]
        recency_col = customer_summary_pr[recency_colname]
        T_col = customer_summary_pr[T_colname]

        self.bgf.fit(frequency_col, recency_col, T_col)

    def plot_frequency_recency_matrix(self, BetaGeoFitter = None):
        """
        Plot the frequency-recency matrix using the fitted BG/NBD model.

        Parameters:
        - BetaGeoFitter (lifetimes.BetaGeoFitter, optional): An instance of the BetaGeoFitter model. If not provided,
          the internal BetaGeoFitter instance associated with the CLTVModel will be used.

        Returns:
            None
        """
        if BetaGeoFitter is None:
            BetaGeoFitter = self.bgf
        plot_frequency_recency_matrix(BetaGeoFitter)
        plt.show()

    def plot_probability_alive_matrix(self, BetaGeoFitter = None):
        """
        Plot the probability alive matrix using the fitted BG/NBD model.

        Parameters:
        - BetaGeoFitter (lifetimes.BetaGeoFitter, optional): An instance of the BetaGeoFitter model. If not provided,
          the internal BetaGeoFitter instance associated with the CLTVModel will be used.

        Returns:
            None
        """
        if BetaGeoFitter is None:
            BetaGeoFitter = self.bgf

        plot_probability_alive_matrix(BetaGeoFitter)
        plt.show()

    def predict_purchases(self, t=1, customer_summary_pr=None, frequency_col=None, recency_col=None, T_col=None, predicted_purchases_colname='predicted_purchases'):
        """
        Predict the number of purchases a customer will make in the future.

        Parameters:
            - t (int, optional): Time period for future predictions. Default is 1.
            - customer_summary_pr (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary_pr' attribute.
            - frequency_col (pd.Series, optional): Series containing customer transaction frequency. Default is the 'frequency' attribute.
            - recency_col (pd.Series, optional): Series containing recency (time since the last transaction). Default is the 'recency' attribute.
            - T_col (pd.Series, optional): Series containing T (age of the customer). Default is the 'T' attribute.
            - predicted_purchases_colname (str, optional): Column name for predicted purchases. Default is 'predicted_purchases'.

        Returns:
            pd.DataFrame: Customer summary DataFrame sorted by predicted purchases.
        """
        if customer_summary_pr is None:
            customer_summary_pr = self.customer_summary_pr
        if frequency_col is None:
            frequency_col = self.frequency
        if frequency_col.name not in customer_summary_pr.columns:
            raise ValueError(f"The {frequency_col.name} column is required in {customer_summary_pr}.")
        if recency_col is None:
            recency_col = self.recency
        if recency_col.name not in customer_summary_pr.columns:
            raise ValueError(f"The {recency_col.name} column is required in {customer_summary_pr}.")
        if T_col is None:
            T_col = self.T
        if T_col.name not in customer_summary_pr.columns:
            raise ValueError(f"The {T_col.name} column is required in {customer_summary_pr}.")

        customer_summary_pr[predicted_purchases_colname] = self.bgf.conditional_expected_number_of_purchases_up_to_time(
            t, frequency_col, recency_col, T_col)
        self.predicted_purchases = customer_summary_pr[predicted_purchases_colname]
        return customer_summary_pr.sort_values(by=predicted_purchases_colname)
 
    def plot_period_transactions(self, BetaGeoFitter = None):
        """
        Plot the actual and predicted number of transactions in each time period.

        Parameters:
        - BetaGeoFitter (lifetimes.BetaGeoFitter, optional): An instance of the BetaGeoFitter model. If not provided,
          the internal BetaGeoFitter instance associated with the CLTVModel will be used.

        Returns:
            None
        """
        if BetaGeoFitter is None:
            BetaGeoFitter = self.bgf

        plot_period_transactions(BetaGeoFitter)
        plt.show()

    def fit_ggf_model(self, customer_summary_pr=None, frequency_colname="frequency", monetary_colname="monetary"):
        """
        Fit the Gamma-Gamma Fitter (GGF) model using the provided frequency and monetary values.

        Parameters:
            - customer_summary_pr (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary_pr' attribute.
            - frequency_colname (str, optional): Column name for customer transaction frequency. Default is 'frequency'.
            - monetary_colname (str, optional): Column name for customer monetary value. Default is 'monetary'.

        Returns:
            None
        """
        if customer_summary_pr is None:
            customer_summary_pr = self.customer_summary_pr
        
        frequency_col = customer_summary_pr[frequency_colname]
        monetary_col = customer_summary_pr[monetary_colname]

        self.ggf.fit(frequency_col, monetary_col)

    def calculate_expected_average_profit(self,customer_summary_pr = None, 
                      frequency_colname="frequency", monetary_colname="monetary",
                      exp_avg_profit_colname = "expected_average_profit"):
        """
        Calculate the expected average profit per transaction.

        Parameters:
            - customer_summary_pr (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary_pr' attribute.
            - frequency_colname (str, optional): Column name for customer transaction frequency. Default is 'frequency'.
            - monetary_colname (str, optional): Column name for customer monetary value. Default is 'monetary'.
            - exp_avg_profit_colname (str, optional): Column name for expected average profit. Default is 'expected_average_profit'.

        Returns:
            pd.DataFrame: Customer summary DataFrame sorted by expected average profit (descending).
        """
        if customer_summary_pr is None:
            customer_summary_pr = self.customer_summary_pr
        
        frequency_col = customer_summary_pr[frequency_colname]
        monetary_col = customer_summary_pr[monetary_colname]
        exp_avg_profit = self.ggf.conditional_expected_average_profit(frequency_col, monetary_col)
        customer_summary_pr[exp_avg_profit_colname] = exp_avg_profit
        return customer_summary_pr.sort_values(exp_avg_profit_colname,
                                               ascending=False)

    def calculate_cltv_prediction(self, time_period=12, discount_rate=0.01, freq="W",
                              frequency_col=None, recency_col=None, T_col=None, monetary_col=None):
        """
        Calculate Customer Lifetime Value (CLTV) predictions using the fitted models.

        Parameters:
            - time_period (int, optional): Time period for CLTV predictions. Default is 12.
            - discount_rate (float, optional): Discount rate for future cash flows. Default is 0.01.
            - freq (str, optional): Frequency of time periods. Default is "W" (weekly).
            - frequency_col (pd.Series, optional): Series containing customer transaction frequency. Default is the 'frequency' attribute.
            - recency_col (pd.Series, optional): Series containing recency (time since the last transaction). Default is the 'recency' attribute.
            - T_col (pd.Series, optional): Series containing T (age of the customer). Default is the 'T' attribute.
            - monetary_col (pd.Series, optional): Series containing customer monetary value. Default is the 'monetary' attribute.

        Returns:
            pd.DataFrame: CLTV predictions for each customer.
        """

        if frequency_col is None:
            frequency_col = self.frequency
        if recency_col is None:
            recency_col = self.recency
        if T_col is None:
            T_col = self.T
        if monetary_col is None:
            monetary_col = self.monetary

        cltv_pred = self.ggf.customer_lifetime_value(
            self.bgf, frequency_col, recency_col,
            T_col, monetary_col,
            time=time_period, freq=freq, discount_rate=discount_rate
        )
        cltv_pred = cltv_pred.reset_index()
        self.cltv_pred = cltv_pred
        return cltv_pred

    def merge_cltv_predictions(self, cltv_pred = None, customer_summary_pr = None, df = None, customer_id_col = "customer_id", how = 'left'):
        """
        Merge CLTV predictions with the original DataFrame.

        Parameters:
            - cltv_pred (pd.DataFrame, optional): CLTV predictions DataFrame. Default is the 'cltv_pred' attribute.
            - customer_summary_pr (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary_pr' attribute.
            - df (pd.DataFrame, optional): Original DataFrame containing customer data. Default is the 'df' attribute.
            - customer_id_col (str, optional): Column name for customer ID. Default is "customer_id".
            - how (str, optional): Type of merge to be performed (e.g., 'left', 'right', 'outer', 'inner'). Default is 'left'.

        Returns:
            None
        """
        if customer_summary_pr is None:
            customer_summary_pr = self.customer_summary_pr
        if df is None:
            df = self.df
        if customer_id_col not in df.columns:
            raise ValueError(f"The {customer_id_col} column is required in {df}.")
        if cltv_pred is None:
            cltv_pred = self.cltv_pred
        
        customer_summary_pr = customer_summary_pr.merge(cltv_pred, on = customer_id_col, how=how)
        self.customer_summary_pr = customer_summary_pr
        return customer_summary_pr

    def create_segments(self, customer_summary_pr = None, clv_col = 'clv', segment_colname = 'segment', num_segments = 4, labels = ["D", "C", "B", "A"]):
        """
        Create customer segments based on CLTV predictions.

        Parameters:
            - customer_summary_pr (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary_pr' attribute.
            - clv_col (str, optional): Column name for Customer Lifetime Value (CLV). Default is 'clv'.
            - segment_colname (str, optional): Column name for the created segment. Default is 'segment'.
            - num_segments (int, optional): Number of segments to create. Default is 4.
            - labels (list, optional): Labels for the created segments. Default is ["D", "C", "B", "A"].

        Returns:
            None
        """
        if customer_summary_pr is None:
            customer_summary_pr = self.customer_summary_pr

        customer_summary_pr[segment_colname] = pd.qcut(customer_summary_pr[clv_col],
                                                        q = num_segments, labels=labels)
        self.segment = customer_summary_pr[segment_colname]

        return customer_summary_pr.sort_values(by=clv_col, ascending=False)

    def display_segments_summary(self, segment_col = None, customer_summary_pr = None):
        """
        Display a summary of customer segments, including count, mean, and sum.

        Parameters:
            - segment_col (pd.Series, optional): Series containing customer segments. Default is the 'segment' attribute.
            - customer_summary_pr (pd.DataFrame, optional): Customer summary DataFrame. Default is the 'customer_summary_pr' attribute.

        Returns:
            pd.DataFrame: Summary statistics for each customer segment.
        """
        if customer_summary_pr is None:
            customer_summary_pr = self.customer_summary_pr
        if segment_col is None:
            segment_col = self.segment
        if segment_col.name not in customer_summary_pr.columns:
            raise ValueError(f"The {segment_col.name} column is required in {customer_summary_pr}.")
        
        return customer_summary_pr.groupby(segment_col.name).agg({"count", "mean", "sum"})

