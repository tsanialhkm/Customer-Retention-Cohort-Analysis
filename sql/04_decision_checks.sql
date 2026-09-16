-- CASE 002: Quantify coverage, limitations, and evidence for the decision.

SELECT
    strftime('%Y-%m', ordered_at) AS order_month,
    COUNT(*) AS order_count
FROM orders
GROUP BY strftime('%Y-%m', ordered_at)
ORDER BY order_month;
