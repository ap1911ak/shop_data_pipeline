import pandas as pd
from prefect import task

@task(name="Drop Old Data", description="Remove old records from the DataFrame")
def drop_old_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove old records from the DataFrame"""
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    df_sorted = df.sort_values(by='signup_date', ascending=True)
    df_cleaned = df_sorted.drop_duplicates(subset=['customer_id'], keep='last')
    return df_cleaned

@task(name="Phone Number Formatting", description="Standardize the phone column to remove all non-numeric characters")
def phone_number_formatting(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize the phone column to remove all non-numeric characters"""
    df['phone_number'] = df['phone_number'].str.replace(r'\D', '', regex=True)
    return df

@task(name="Fill Email Nulls", description="Replace missing emails with 'unknown@domain.com'")
def fill_email_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Replace missing emails with 'unknown@domain.com'"""
    df['email'] = df['email'].fillna('unknown@domain.com')
    df['email'] = df['email'].replace('NaN', 'unknown@domain.com')
    return df  

@task(name="Drop Negative", description="Filter out any orders with a total_amount less than or equal to zero")
def drop_negative(df: pd.DataFrame) -> pd.DataFrame:
    """Filter out any orders with a total_amount less than or equal to zero"""
    return df[df["total_amount"] > 0]  

@task(name="Convert to USD", description="Convert the total_amount column from THB to USD using a fixed exchange rate of 0.03")
def convert_to_usd(df: pd.DataFrame) -> pd.DataFrame:
    df["total_amount_usd"] = df.apply(
        lambda row: row["total_amount"]
        if row["currency"] == "USD"
        else row["total_amount"] * row["rate_to_usd"],
        axis=1,
    )
    df = df.drop(columns=['total_amount'])
    df = df.drop(columns=['currency'])
    df = df.drop(columns=['rate_to_usd'])
    return df
