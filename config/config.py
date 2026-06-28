import os

class Config:
    rawDB = os.path.join('data', 'raw', 'shopdata.db')
    rawTable = ["raw_customers", "exchange_rates", "raw_orders"]
    cleanDB = os.path.join('data', 'cleaned', 'analytics.db')
    cleanTable = ["dim_customers", "fct_orders"]
