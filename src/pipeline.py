import sqlite3
from config import config
from prefect import flow
from src.extract import extract_table
from src.transform import *

@flow(name="Shop Data Pipeline", log_prints=True)
def shop_data_pipeline(raw_db_path: str, raw_table_customers: str, raw_table_exchange_rates: str, raw_table_orders: str, clean_table_customers: str, clean_table_orders: str):
    # Connect to the raw database
    conn = sqlite3.connect(raw_db_path)
    print(f"Connected to raw database: {raw_db_path}")

    # Extract data from the raw tables
    df_customers = extract_table(conn, raw_table_customers)
    df_exchange_rates = extract_table(conn, raw_table_exchange_rates)
    df_orders = extract_table(conn, raw_table_orders)

    # print(df_customers.head())
    # print(df_exchange_rates.head())
    # print(df_orders.head())

    # Transform the data
    df_cleaned_customers = drop_old_data(df_customers)
    df_cleaned_customers = phone_number_formatting(df_cleaned_customers)
    df_cleaned_customers = fill_email_nulls(df_cleaned_customers)

    print(df_cleaned_customers.head())

    df_cleaned_orders = df_orders.merge(df_exchange_rates, on='currency', how='left')
    print(f"\nCleaned Orders:\n{df_cleaned_orders.head()}")
    
    df_cleaned_orders = drop_negative(df_cleaned_orders)
    df_cleaned_orders = convert_to_usd(df_cleaned_orders)

    print(f"\nCleaned Orders:\n{df_cleaned_orders.head()}")


if __name__ == "__main__":
    
    raw_db_path = config.Config.rawDB
    clean_db_path = config.Config.cleanDB
    raw_table_customers = config.Config.rawTable[0]
    raw_table_exchange_rates = config.Config.rawTable[1]
    raw_table_orders = config.Config.rawTable[2]
    clean_table_customers = config.Config.cleanTable[0]
    clean_table_orders = config.Config.cleanTable[1]
    
    shop_data_pipeline(raw_db_path, raw_table_customers,raw_table_exchange_rates,raw_table_orders,clean_table_customers,clean_table_orders)

    