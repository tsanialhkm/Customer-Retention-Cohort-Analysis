-- CASE 002: Build and test a comparable retention definition.

SELECT
    customer_id,
    first_observed_order_at,
    first_observed_order_id,
    home_country
FROM customer_accounts
ORDER BY first_observed_order_at
LIMIT 20;
