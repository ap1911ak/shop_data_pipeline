import pytest
import pandas as pd
from src.transform import drop_old_data, phone_number_formatting, fill_email_nulls, drop_negative, convert_to_usd

def test_drop_old_data():
    """Remove old records"""
    mock_data = pd.DataFrame({
        "customer_id": [1, 2, 2, 3],
        "signup_date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
        "email": ["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]
    })

    cleaned_df = drop_old_data(mock_data)

    assert cleaned_df.loc[cleaned_df["customer_id"] == 1, "email"].iloc[0] == "user1@example.com"
    assert cleaned_df.loc[cleaned_df["customer_id"] == 2, "email"].iloc[0] == "user3@example.com"
    assert cleaned_df.loc[cleaned_df["customer_id"] == 3, "email"].iloc[0] == "user4@example.com"

def test_phone_number_formatting():
    """Standardize the phone column to remove all non-numeric characters"""
    
    mock_data = pd.DataFrame({
        "customer_id": [1, 2, 3],
        "phone": ["0812345678", "0812345678", "+11(083) 456-7890"]
    })

    formatted_df = phone_number_formatting(mock_data)

    expected_numbers = ["0812345678", "0812345678", "110834567890"]
    assert formatted_df["phone"].tolist() == expected_numbers

def test_fill_email_nulls():
    """Replace missing emails with "unknown@domain.com"."""

    mock_data = pd.DataFrame({
        "customer_id": [1, 2, 3],
        "email": ["user1@example.com", None, "NaN"]
    })

    filled_df = fill_email_nulls(mock_data)

    assert filled_df["email"].tolist() == ["user1@example.com", "unknown@domain.com", "unknown@domain.com"]

def test_drop_negative():
    """Filter out any orders with a total_amount less than or equal to zero"""
    mock_data = pd.DataFrame({
        "product_id": [1, 2, 2, 3],
        "product_name": ["Cake", "Brownie", "Brownie", "Cookie"],
        "total_amount": [120.0, -50.0, -50.0, 45.0]
    })

    cleaned_df = drop_negative(mock_data)

    assert len(cleaned_df) == 2
    assert cleaned_df.loc[cleaned_df["product_id"] == 1, "product_name"].iloc[0] == "Cake"
    assert cleaned_df.loc[cleaned_df["product_id"] == 3, "product_name"].iloc[0] == "Cookie"

def test_convert_to_usd():
    """Convert the total_amount column from THB to USD using a fixed exchange rate of 0.03"""
    mock_data_order = pd.DataFrame({
        "total_amount": [1000.0, 2000.0, 3000.0],
        "currency": ["USD", "JPY", "THB"],
        "rate_to_usd": [1.0, 0.009, 0.03],
        "date": ["2023-01-01", "2023-01-02", "2023-01-03"]
    })

    converted_df = convert_to_usd(mock_data_order)

    
    expected_amounts = [1000.0, 18.0, 90.0]  
    assert converted_df["total_amount_usd"].tolist() == expected_amounts