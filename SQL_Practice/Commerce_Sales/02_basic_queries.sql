-- Q1. List paid orders and their payment amounts, ordered by order ID.
SELECT
    O.order_id,
    O.service_name,
    O.customer_id,
    O.ordered_at,
    P.amount
FROM de_practice.orders O
JOIN de_practice.payments P
    ON O.order_id = P.order_id
WHERE P.status = 'PAID'
ORDER BY O.order_id ASC;

-- Q2. Count paid orders and sum paid amounts by order date.
SELECT
    O.ordered_at,
    COUNT(*) AS payment_count,
    SUM(P.amount) AS total_amount
FROM de_practice.orders O
JOIN de_practice.payments P
    ON O.order_id = P.order_id
WHERE P.status = 'PAID'
GROUP BY O.ordered_at
ORDER BY O.ordered_at ASC;
