"""
SQLite Database Handler Module

This module defines the SqlHandler class, which handles SQLite database operations,
including table manipulation and data import/export.

Classes:
- SqlHandler: Handles SQLite database operations, including table manipulation
  and data import/export.

Note:
- This module assumes that the database connection is established
  using the SqlHandler class and follows a specific structure.
"""

import sqlite3
import logging
import pandas as pd
import numpy as np
import os
from ..Logger import CustomFormatter

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


class SqlHandler:
    """
    Handles SQLite database operations including
    table manipulation and data import/export.
    """
    def __init__(self, dbname: str, table_name: str or list) -> None:
        """
        Initializes the SqlHandler object.

        Args:
            dbname (str): Name of the SQLite database.
            table_name (str or list): Name of the table(s) to be operated upon.
        """
        self.cnxn = sqlite3.connect(f'{dbname}.db')
        self.cursor = self.cnxn.cursor()
        self.dbname = dbname
        self.table_name = table_name

    def close_cnxn(self) -> None:
        """
        Closes the database connection.
        """
        logger.info('commiting the changes')
        self.cursor.close()
        self.cnxn.close()
        logger.info('the connection has been closed')

    def get_table_columns(self) -> list:
        """
        Retrieves column names of the specified table.

        Returns:
            list: List of column names.
        """
        self.cursor.execute(f"PRAGMA table_info({self.table_name});")
        columns = self.cursor.fetchall()

        column_names = [col[1] for col in columns]
        logger.info(f'the list of columns: {column_names}')
        # self.cursor.close()

        return column_names

    def truncate_table(self) -> None:
        """
        Truncates the specified table.
        """
        query = f"DROP TABLE IF EXISTS {self.table_name};"
        self.cursor.execute(query)
        logging.info(f'the {self.table_name} is truncated')
        # self.cursor.close()

    def drop_table(self):
        """
        Drops the specified table from the database.

        This method executes an SQL query to drop the table
        specified by the 'table_name' attribute.

        Raises:
            Exception: If an error occurs while dropping the table.

        Note:
            - Ensure that the 'table_name' attribute
            is properly set before calling this method.
            - This operation is irreversible and
            permanently deletes the specified table.
        """
        query = f"DROP TABLE IF EXISTS {self.table_name};"
        logging.info(query)

        self.cursor.execute(query)

        self.cnxn.commit()

        logging.info(f"table '{self.table_name}' deleted.")
        logger.debug('using drop table function')

    def insert_many(self, df: pd.DataFrame) -> str:
        """
        Inserts multiple rows into the specified table
        based on the given Pandas DataFrame.

        Args:
            df (pd.DataFrame): Pandas DataFrame
            containing the data to be inserted.

        Raises:
            Exception: If an error occurs
            while inserting the data into the table.
        """
        df = df.replace(np.nan, None)  # for handling NULLS
        df.rename(columns=lambda x: x.lower(), inplace=True)
        columns = list(df.columns)
        logger.info(f'BEFORE the column intersection: {columns}')
        sql_column_names = [i.lower() for i in self.get_table_columns()]
        columns = list(set(columns) & set(sql_column_names))
        logger.info(f'AFTER the column intersection: {columns}')
        ncolumns = list(len(columns)*'?')
        data_to_insert = df.loc[:, columns]

        values = [tuple(i) for i in data_to_insert.values]
        logger.info(f'''the shape of the table
                    which is going to be imported {data_to_insert.shape}''')

        if len(columns) > 1:
            cols, params = ', '.join(columns), ', '.join(ncolumns)
        else:
            cols, params = columns[0], ncolumns[0]

        logger.info(f'insert structure: colnames: {cols} params: {params}')
        logger.info(values[0])
        query = f"""INSERT INTO  {self.table_name}
        ({cols}) VALUES ({params});"""

        logger.info(f'QUERY: {query}')

        self.cursor.executemany(query, values)
        try:
            for i in self.cursor.messages:
                logger.info(i)
        except:
            pass

        self.cnxn.commit()

        logger.warning('the data is loaded')

    def from_sql_to_pandas(self, chunksize: int,
                           id_value: str) -> pd.DataFrame:
        """
        Retrieves data from the specified table in chunks
        and converts it into a Pandas DataFrame.

        Args:
            chunksize (int): Number of rows to fetch in each chunk.
            id_value (str): Column name to be used for
            ordering and fetching data in chunks.

        Returns:
            pd.DataFrame: Concatenated Pandas DataFrame
            containing the selected data.
        """
        offset = 0
        dfs = []

        while True:
            query = f"""
            SELECT * FROM {self.table_name}
                ORDER BY {id_value}
                OFFSET  {offset}  ROWS
                FETCH NEXT {chunksize} ROWS ONLY
            """
            data = pd.read_sql_query(query, self.cnxn)
            logger.info(f'the shape of the chunk: {data.shape}')
            dfs.append(data)
            offset += chunksize
            if len(dfs[-1]) < chunksize:
                logger.warning('loading the data from SQL is finished')
                logger.debug('connection is closed')
                break
        df = pd.concat(dfs)

        return df

    def select_by_id(id: int, db_name: str, table_name: str, table_id: str):
        """
        Selects a row from the specified table based on the given ID.

        Args:
            id (int): ID value to be used in the WHERE clause.
            db_name (str): Name of the SQLite database.
            table_name (str): Name of the table to be queried.
            table_id (str): Name of the column
            representing the ID in the table.

        Returns:
            dict: Dictionary containing the selected data.
        """
        db = sqlite3.connect(db_name)
        db.row_factory = sqlite3.Row  # Return rows as dictionaries
        db_cursor = db.cursor()

        query = f"""
        SELECT * FROM {table_name} WHERE {table_id} = {id};
        """
        try:
            db_cursor.execute(query)
            selected_data = db_cursor.fetchone()
            logger.info(f'Id {id} selected successfully')
            return {"data": selected_data}
        except Exception as e:
            logger.info(f"Error selecting id: {str(e)}")

    def select_many(start_id: int, head: int,
                    db_name: str, table_name: str, table_id: str):
        """
        Selects multiple rows from the specified table
        based on the start ID and the number of rows.

        Args:
            start_id (int): Starting ID value for the selection.
            head (int): Number of rows to be retrieved.
            db_name (str): Name of the SQLite database.
            table_name (str): Name of the table to be queried.
            table_id (str): Name of the column
            representing the ID in the table.

        Returns:
            dict: Dictionary containing the selected data.
        """
        db = sqlite3.connect(db_name)
        db.row_factory = sqlite3.Row  # Return rows as dictionaries
        db_cursor = db.cursor()

        query = f"""
        SELECT * FROM {table_name}
        WHERE {table_id} >= {start_id} LIMIT {head+1};
        """
        try:
            db_cursor.execute(query)
            selected_data = db_cursor.fetchall()

            results = []
            for row in selected_data:
                result = dict(row)
                results.append(result)

            logger.info(f"""Rows starting from ID {start_id}
                        selected successfully""")
            return {"data": results}
        except Exception as e:
            logger.info(f"Error selecting rows: {str(e)}")

    def delete_by_id(id: int, db_name: str, table_name: str, table_id: str):
        """
        Deletes a row from the specified table based on the given ID.

        Args:
            id (int): ID value to be used in the WHERE clause.
            db_name (str): Name of the SQLite database.
            table_name (str): Name of the table to be deleted from.
            table_id (str): Name of the column
            representing the ID in the table.
        """
        db = sqlite3.connect(db_name)
        db_cursor = db.cursor()
        query = f"""
        DELETE FROM {table_name}
        WHERE {table_id} = {id};
        """
        try:
            db_cursor.execute(query)
            db.commit()
            logger.info(f'Id {id} deleted successfully')
        except Exception as e:
            logger.info(f"Error deleting id: {str(e)}")

    def update_by_id(id: int, update_values: dict,
                     db_name: str, table_name: str, table_id: str):
        """
        Updates a row in the specified table
        based on the given ID and update values.

        Args:
            id (int): ID value to be used in the WHERE clause.
            update_values (dict): Dictionary containing column names as keys
            and new values as values.
            db_name (str): Name of the SQLite database.
            table_name (str): Name of the table to be updated.
            table_id (str): Name of the column
            representing the ID in the table.
        """
        db = sqlite3.connect(db_name)
        db_cursor = db.cursor()

        update_values = update_values.model_dump(
            exclude_unset=True, exclude_defaults=True, exclude_none=True)

        columns_to_update = ", ".join([f"{column} = '{update_values[column]}'"
                                       for column in update_values.keys()])

        query = f"""UPDATE {table_name}
                    SET {columns_to_update}
                    WHERE {table_id} = '{id}'"""
        try:
            db_cursor.execute(query)
            db.commit()
            db.close()
            logger.info(f'''Row with ID {id}
                        updated successfully for specified columns''')
        except Exception as e:
            logger.info(f"Error updating row: {str(e)}")

    def insert_by_id(insert_values: dict, db_name: str, table_name: str):
        """
        Inserts a new row into the specified table based on the given values.

        Args:
            insert_values (dict): Dictionary containing column names as keys
            and values to be inserted as values.
            db_name (str): Name of the SQLite database.
            table_name (str): Name of the table to insert the new row into.
        """
        db = sqlite3.connect(db_name)
        db_cursor = db.cursor()

        insert_values = insert_values.model_dump(
            exclude_unset=True, exclude_defaults=True, exclude_none=True)

        columns = ', '.join(insert_values.keys())
        values = ', '.join([f"'{value}'" for value in insert_values.values()])

        query = f"""INSERT INTO {table_name} ({columns})
                    VALUES ({values})"""

        try:
            db_cursor.execute(query)
            db.commit()
            db.close()
            logger.info('Row inserted successfully')
        except Exception as e:
            logger.info(f"Error inserting row: {str(e)}")

    def execute_custom_query(self, query, conn_string='temp.db'):
        """
        Executes a custom SQL query on the specified database connection.

        Args:
            query (str): SQL query to be executed.
            conn_string (str): Database connection string
            (default is 'temp.db').

        Returns:
            list: List of query results.
        """
        conn = sqlite3.connect(conn_string)
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        conn.close()
        logger.info(f'Executed custom query: {query}')

        return results
