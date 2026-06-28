import sqlite3
from config import config
from load import create_db, load_table
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
    conn.close()

    print(df_cleaned_customers.head())

    df_cleaned_orders = df_orders.merge(df_exchange_rates, on='currency', how='left')
    print(f"\nCleaned Orders:\n{df_cleaned_orders.head()}")
    
    df_cleaned_orders = drop_negative(df_cleaned_orders)
    df_cleaned_orders = convert_to_usd(df_cleaned_orders)

    print(f"\nCleaned Orders:\n{df_cleaned_orders.head()}")


    # Load the cleaned data into the clean database
    clean_conn =create_db(config.Config.cleanDB)
    load_table(clean_conn, df_cleaned_customers, clean_table_customers)
    load_table(clean_conn, df_cleaned_orders, clean_table_orders)

    # check the loaded data in the clean database
    # cursor = clean_conn.cursor()
    # cursor.execute(f"SELECT * FROM {clean_table_customers} LIMIT 5")
    # print(f"\nSample data from '{clean_table_customers}':\n{cursor.fetchall()}")
    # cursor.execute(f"SELECT * FROM {clean_table_orders} LIMIT 5")
    # print(f"\nSample data from '{clean_table_orders}':\n{cursor.fetchall()}")
    clean_conn.close()

if __name__ == "__main__":
    
    raw_db_path = config.Config.rawDB
    clean_db_path = config.Config.cleanDB
    raw_table_customers = config.Config.rawTable[0]
    raw_table_exchange_rates = config.Config.rawTable[1]
    raw_table_orders = config.Config.rawTable[2]
    clean_table_customers = config.Config.cleanTable[0]
    clean_table_orders = config.Config.cleanTable[1]
    
    shop_data_pipeline(raw_db_path, raw_table_customers,raw_table_exchange_rates,raw_table_orders,clean_table_customers,clean_table_orders)

    