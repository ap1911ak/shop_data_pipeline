import sqlite3
import pandas as pd
from config.config import Config

def extract_table(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    """ดึงข้อมูลจากตารางที่กำหนดใน SQLite ออกมาเป็น pandas DataFrame"""
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    return df

conn = sqlite3.connect(Config.rawDB)
df = extract_table(conn, "raw_orders")
print(df.head())