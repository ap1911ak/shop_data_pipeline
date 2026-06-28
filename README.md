# shop_data_pipeline
---------------------
## Discription
This repository manages an automated **ETL (Extract, Transform, Load) Pipeline** designed for an e-commerce platform's data ecosystem. The system ingests unstable, multi-currency transactional data, applies programmatic data cleansing to handle operational anomalies, and transforms it into a clean.



## ⛃ Soure
shopdata.db
A relational database for order data of ShopData Inc.



## 🏗️ Structure and Meta data

### 1. `raw_customers` Table
Stores raw profile information of users.
| Table Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `customer_id` | INTEGER | Identifier for each customer |
| `full_name` | TEXT | First and last name of the customer |
| `email` | TEXT | Email address of the customer |
| `phone` | TEXT | Contact telephone number |
| `signup_date` | TEXT | Registration timestamp (`YYYY-MM-DD`) |

### 2. `exchange_rates` Table
Records historical daily exchange rates the US Dollar.

| Table Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `currency` | TEXT | 3-letter ISO currency code (e.g., `EUR`, `JPY`) |
| `rate_to_usd` | REAL | Exchange rate the currency to USD |
| `date` | TEXT | The effective date of the exchange rate (`YYYY-MM-DD`) |

### 3. `raw_orders` Table
Raw transactio logs and processing statuses for all orders.

| Table Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `order_id` | INTEGER | Identifier for each order invoice|
| `customer_id` | INTEGER | Reference ID linking the customer table|
| `order_date` | TEXT | Timestamp when the transaction (`YYYY-MM-DD') |
| `total_amount` | REAL | Total checkout amount in the transaction |
| `currency` | TEXT | The currency code used by the customer to pay for the order |
| `status` | TEXT | State of the transaction (e.g., `COMPLTE`, `ERROR`) |



## 🔍 Data Validation Report (การตรวจสอบข้อมูลเบื้องต้น)

This section tracks the data quality and anomalies found during the initial data profiling stage. Below is the summary of data integrity checks executed on the current raw dataset:

| Validation Rule / Check Item | Issue Count | Status | Description |
| :--- | :---: | :---: | :--- |
| **Missing Customer** | 3 | ⚠️ Warning | Critical profile fields (e.g., Email, Name) contain NULL or empty values. |
| **Missing Exchange Rate** | 0 | ✅ Passed | All transaction currencies have a valid matching rate for their transaction dates. |
| **Missing Order** | 3 | ⚠️ Warning | Found blank or incomplete records within core transaction fields. |
| **Negative Exchange Rate** | 0 | ✅ Passed | No corrupted zero or negative values found in currency multipliers. |
| **Negative total_amount** | 2 | ❌ Failed | Found 2 orders with negative transaction amounts (requires refund/void logic check). |
| **Date Format (Customer)** | 0 | ✅ Passed | All customer `signup_date` strings strictly comply with the standard date format. |
| **Date Format (Order)** | 0 | ✅ Passed | All `order_date` values are well-formatted and parsable. |
| **In Orders No Customer ** | 2 | ❌ Failed | Found 2 transactions mapped to `customer_id` values that do not exist in the customer database. |
