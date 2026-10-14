-- Q3. Daily net revenue (order-date basis).
-- Why pre-aggregate refunds? Order 102 has 2 refund rows.
-- Joining raw refunds to payments would duplicate payment amount 50,000.
WITH refund_summary AS (
    SELECT
        order_id,
        SUM(refund_amount) AS refund_total
    FROM de_practice.refunds
    GROUP BY order_id
)
SELECT
    O.ordered_at,
    SUM(P.amount) AS total_amount,
    COALESCE(SUM(R.refund_total), 0) AS total_refund,
    SUM(P.amount) - COALESCE(SUM(R.refund_total), 0) AS net_revenue
FROM de_practice.orders O
JOIN de_practice.payments P
    ON O.order_id = P.order_id
LEFT JOIN refund_summary R
    ON O.order_id = R.order_id
WHERE P.status = 'PAID'
GROUP BY O.ordered_at
ORDER BY O.ordered_at ASC;

-- Q4. Daily net revenue by service.
WITH refund_summary AS (
    SELECT
        order_id,
        SUM(refund_amount) AS refund_total
    FROM de_practice.refunds
    GROUP BY order_id
)
SELECT
    O.service_name,
    O.ordered_at,
    COUNT(*) AS payment_count,
    SUM(P.amount) AS total_amount,
    COALESCE(SUM(R.refund_total), 0) AS total_refund,
    SUM(P.amount) - COALESCE(SUM(R.refund_total), 0) AS net_revenue
FROM de_practice.orders O
JOIN de_practice.payments P
    ON O.order_id = P.order_id
LEFT JOIN refund_summary R
    ON O.order_id = R.order_id
WHERE P.status = 'PAID'
GROUP BY O.service_name, O.ordered_at
ORDER BY O.ordered_at ASC, O.service_name ASC;
