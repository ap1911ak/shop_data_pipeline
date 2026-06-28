import os
import sqlite3
import pandas as pd
from config.config import Config

def create_db(db_path: str) -> sqlite3.Connection:
    folder = os.path.dirname(db_path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    conn = sqlite3.connect(db_path)
    print(f"Connected to database: {db_path}")
    return conn

def load_table(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str):
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data loaded into table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error occurred while loading data into table '{table_name}': {e}")