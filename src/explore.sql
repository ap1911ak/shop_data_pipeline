.schema raw_customers
.schema exchange_rates
.schema raw_orders

SELECT 'missing customer' AS issue_type, COUNT(*) AS anomaly_count
FROM raw_customers
WHERE customer_id IS NULL OR full_name IS NULL OR email IS NULL OR phone IS NULL OR signup_date IS NULL;

SELECT 'missing exchange rate' AS issue_type, COUNT(*) AS anomaly_count
FROM exchange_rates
WHERE currency IS NULL OR rate_to_usd IS NULL;

SELECT 'missing order' AS issue_type, COUNT(*) AS anomaly_count
FROM raw_orders
WHERE order_id IS NULL OR customer_id IS NULL OR order_date IS NULL OR total_amount IS NULL OR currency IS NULL OR status IS NULL;  

SELECT 'Negative Exchange Rate' AS issue_type, COUNT(*)
FROM exchange_rates
WHERE rate_to_usd < 0;

SELECT 'Negative total_amount' AS issue_type, COUNT(*)
FROM raw_orders
WHERE total_amount < 0;

SELECT 'Date Format customer' AS issue_type, COUNT(*)
FROM raw_customers
WHERE length(signup_date) != 10 OR signup_date NOT LIKE '____-__-__';

SELECT 'Date Format order' AS issue_type, COUNT(*)
FROM raw_orders
WHERE length(order_date) != 10 OR order_date NOT LIKE '____-__-__';

SELECT 'In Orders No Customer)' AS issue_type, COUNT(*)
FROM raw_orders o
LEFT JOIN raw_customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

SELECT 'Customer phone not Int' AS issue_type, COUNT(*)
FROM raw_customers
WHERE phone IS NOT NULL AND phone NOT REGEXP '^[0-9]+$';