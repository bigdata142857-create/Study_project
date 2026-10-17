-- Q3. Show the previous status of each order event.
-- LAG() takes a column argument. The first event has no previous status (NULL).
SELECT
    event_id,
    order_id,
    status,
    LAG(status) OVER (
        PARTITION BY order_id
        ORDER BY changed_at ASC, event_id ASC
    ) AS prev_status,
    changed_at
FROM de_practice.order_events
ORDER BY order_id ASC, changed_at ASC, event_id ASC;

-- Q4. Time elapsed from the previous event, in minutes.
-- Step 1: LAG(changed_at) retrieves the previous event timestamp.
-- Step 2: Timestamp subtraction produces an INTERVAL.
-- Step 3: EXTRACT(EPOCH FROM interval) converts it to seconds.
-- Step 4: Divide seconds by 60 to obtain minutes.
-- prev_changed_at is retained as an extra learning/debug column.
SELECT
    event_id,
    order_id,
    LAG(status) OVER (
        PARTITION BY order_id
        ORDER BY changed_at ASC, event_id ASC
    ) AS prev_status,
    status,
    LAG(changed_at) OVER (
        PARTITION BY order_id
        ORDER BY changed_at ASC, event_id ASC
    ) AS prev_changed_at,
    EXTRACT(
        EPOCH FROM (
            changed_at - LAG(changed_at) OVER (
                PARTITION BY order_id
                ORDER BY changed_at ASC, event_id ASC
            )
        )
    ) / 60 AS elapsed_minutes,
    changed_at
FROM de_practice.order_events
ORDER BY order_id ASC, changed_at ASC, event_id ASC;
