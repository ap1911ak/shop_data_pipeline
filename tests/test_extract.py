import pytest
import sqlite3
import pandas as pd
from src.extract import extract_table

@pytest.fixture
def setup_mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE orders (order_id INT, customer_id INT, amount REAL)")
    cursor.execute("INSERT INTO orders VALUES (1, 101, 150.0), (2, 102, 250.5)")
    conn.commit()
    yield conn
    conn.close()

def test_extract_table_success(setup_mock_db):
    conn = setup_mock_db
    
    df = extract_table(conn, "orders")
    
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 3)
    assert list(df.columns) == ["order_id", "customer_id", "amount"]