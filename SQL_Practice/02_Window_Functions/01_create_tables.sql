-- Day 2: Window Functions (PostgreSQL)
-- Learning data only; not sourced from a real business.
-- Run in a scratch DB. Existing tables are not dropped.
CREATE SCHEMA IF NOT EXISTS de_practice;

CREATE TABLE IF NOT EXISTS de_practice.order_events (
    event_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    changed_at TIMESTAMP NOT NULL
);

INSERT INTO de_practice.order_events
    (event_id, order_id, status, changed_at)
VALUES
    (1, 201, 'CREATED',   '2026-10-15 09:00'),
    (2, 202, 'CREATED',   '2026-10-15 09:05'),
    (3, 201, 'PAID',      '2026-10-15 09:10'),
    (4, 203, 'CREATED',   '2026-10-15 09:15'),
    (5, 202, 'PAID',      '2026-10-15 09:20'),
    (6, 201, 'SHIPPED',   '2026-10-15 11:00'),
    (7, 203, 'CANCELED',  '2026-10-15 11:05'),
    (8, 204, 'CREATED',   '2026-10-16 10:00'),
    (9, 204, 'PAID',      '2026-10-16 10:05'),
    (10, 202, 'SHIPPED',  '2026-10-16 14:00'),
    (11, 201, 'DELIVERED','2026-10-16 15:00'),
    (12, 205, 'CREATED',  '2026-10-16 17:00')
ON CONFLICT (event_id) DO NOTHING;

CREATE TABLE IF NOT EXISTS de_practice.customer_orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    amount INT NOT NULL,
    ordered_at TIMESTAMP NOT NULL
);

INSERT INTO de_practice.customer_orders
    (order_id, customer_id, amount, ordered_at)
VALUES
    (301, 101, 120000, '2026-10-01 10:00'),
    (302, 101, 120000, '2026-10-02 11:00'),
    (303, 101, 70000,  '2026-10-03 12:00'),
    (304, 101, 40000,  '2026-10-04 13:00'),
    (305, 102, 90000,  '2026-10-01 14:00'),
    (306, 102, 90000,  '2026-10-02 15:00'),
    (307, 102, 30000,  '2026-10-03 16:00'),
    (308, 103, 150000, '2026-10-01 17:00'),
    (309, 103, 80000,  '2026-10-02 18:00'),
    (310, 103, 80000,  '2026-10-03 19:00')
ON CONFLICT (order_id) DO NOTHING;
