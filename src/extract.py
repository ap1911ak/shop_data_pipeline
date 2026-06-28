import sqlite3
import pandas as pd

def extract_table(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        return df
    except pd.errors.DatabaseError as e:
        raise(f"Not found : '{table_name}': {e}")
        