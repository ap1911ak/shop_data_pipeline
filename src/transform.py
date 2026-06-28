import pandas as pd
from prefect import task, get_run_logger


@task(name="Drop Old Data", description="Remove old records from the DataFrame")
def drop_old_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logger = get_run_logger()
        """Remove old records from the DataFrame"""
        df['signup_date'] = pd.to_datetime(df['signup_date'])
        df_sorted = df.sort_values(by='signup_date', ascending=True)
        df_cleaned = df_sorted.drop_duplicates(subset=['customer_id'], keep='last')
        logger.info("Old records dropped from the DataFrame.")
    except Exception as e:
        logger.error(f"Error occurred while dropping old records: {e}")
    return df_cleaned

@task(name="Phone Number Formatting", description="Standardize the phone column to remove all non-numeric characters")
def phone_number_formatting(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logger = get_run_logger()
        """Standardize the phone column to remove all non-numeric characters"""
        df['phone'] = df['phone'].str.replace(r'\D', '', regex=True)
        logger.info("Phone numbers formatted.")
    except Exception as e:
        logger.error(f"Error occurred while formatting phone numbers: {e}")
    return df


@task(name="Fill Email Nulls", description="Replace missing emails with 'unknown@domain.com'")
def fill_email_nulls(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logger = get_run_logger()
        """Replace missing emails with 'unknown@domain.com'"""
        df['email'] = df['email'].fillna('unknown@domain.com')
        df['email'] = df['email'].replace('NaN', 'unknown@domain.com')
        logger.info("Missing emails filled with 'unknown@domain.com'.")
    except Exception as e:
        logger.error(f"Error occurred while filling missing emails: {e}")
    return df  

@task(name="Drop Negative", description="Filter out any orders with a total_amount less than or equal to zero")
def drop_negative(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logger = get_run_logger()
        """Filter out any orders with a total_amount less than or equal to zero"""
        logger.info("Filtering out negative order amounts.")
        return df[df["total_amount"] > 0]
    except Exception as e:
        logger.error(f"Error occurred while filtering negative order amounts: {e}")
        return df

@task(name="Convert to USD", description="Convert the total_amount column from THB to USD using a fixed exchange rate of 0.03")
def convert_to_usd(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logger = get_run_logger()
        df["total_amount_usd"] = df.apply(
            lambda row: row["total_amount"]
            if row["currency"] == "USD"
            else row["total_amount"] * row["rate_to_usd"],
            axis=1,
        )
        logger.info("Converted total_amount to USD.")

        df = df.drop(columns=['total_amount'])
        df = df.drop(columns=['currency'])
        df = df.drop(columns=['rate_to_usd'])
        df = df.drop(columns=['date'])
        logger.info("Dropped unnecessary columns: total_amount, currency, rate_to_usd, date.")
    except Exception as e:
        logger.error(f"Error occurred while converting total_amount to USD or dropping columns: {e}")
    return df
