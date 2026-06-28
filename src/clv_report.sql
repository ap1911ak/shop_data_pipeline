-- .schema dim_customers
-- .schema fct_orders

SELECT 
    c.customer_id, 
    c.full_name, 
    COUNT(o.order_id) AS total_orders_placed, 
    COALESCE(SUM(o.total_amount_usd), 0) AS lifetime_value_usd
FROM dim_customers c
LEFT JOIN fct_orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.full_name
ORDER BY 
    lifetime_value_usd DESC;