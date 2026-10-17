-- Q1. Find the latest status for each order.
-- ROW_NUMBER() numbers events within an order by newest time and event ID.
-- Filtering rn=1 needs an outer query (CTE here).
WITH ranked_events AS (
    SELECT
        order_id,
        status,
        changed_at,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY changed_at DESC, event_id DESC
        ) AS rn
    FROM de_practice.order_events
)
SELECT
    order_id,
    status,
    changed_at
FROM ranked_events
WHERE rn = 1
ORDER BY order_id ASC;

-- Q2. Rank order amounts within each customer.
-- RANK() skips ranks after ties; DENSE_RANK() does not.
-- Do not add order_id inside the window ORDER BY: ties must stay tied.
SELECT
    customer_id,
    order_id,
    amount,
    RANK() OVER (
        PARTITION BY customer_id
        ORDER BY amount DESC
    ) AS sales_rank,
    DENSE_RANK() OVER (
        PARTITION BY customer_id
        ORDER BY amount DESC
    ) AS sales_dense_rank
FROM de_practice.customer_orders
ORDER BY customer_id ASC, amount DESC, order_id ASC;
