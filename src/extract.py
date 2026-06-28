import sqlite3
import pandas as pd
from prefect import task, get_run_logger

@task(name="Extract Table Data")
def extract_table(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info(f"Extracting data from table: {table_name}")
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        return df
    except pd.errors.DatabaseError as e:
        logger.error(f"Not found : '{table_name}': {e}")
        raise