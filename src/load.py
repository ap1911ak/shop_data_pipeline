import os
import sqlite3
import pandas as pd
from config.config import Config
from prefect import task, get_run_logger
from prefect.cache_policies import NO_CACHE


@task(name="Create Database", description="Create a SQLite database connection",cache_policy=NO_CACHE)
def create_db(db_path: str) -> sqlite3.Connection:
    logger = get_run_logger()
    folder = os.path.dirname(db_path)
    try :
        if not os.path.exists(folder):
            os.makedirs(folder)
            logger.info(f"Created folder for database: {folder}")
    except Exception as e:
        logger.error(f"Error occurred while creating database folder: {e}")
    try:
        conn = sqlite3.connect(db_path)
        logger.info(f"Connected to database: {db_path}")
    except Exception as e:
        logger.error(f"Error occurred while connecting to database: {e}")
    return conn

@task(name="Load Table", description="Load a DataFrame into a SQLite table",cache_policy=NO_CACHE)
def load_table(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str):
    logger = get_run_logger()
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        logger.info(f"Data loaded into table '{table_name}' successfully.")
    except Exception as e:
        logger.error(f"Error occurred while loading data into table '{table_name}': {e}")