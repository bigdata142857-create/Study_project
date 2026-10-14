-- Day 1: Commerce sales SQL practice (PostgreSQL)
-- Run this file first. Sample data is fictional and not from a real company.
-- Run on a scratch database: existing tables are not dropped.
CREATE SCHEMA IF NOT EXISTS de_practice;

CREATE TABLE IF NOT EXISTS de_practice.orders (
    order_id INT PRIMARY KEY,
    service_name VARCHAR(30),
    customer_id INT,
    ordered_at DATE
);

CREATE TABLE IF NOT EXISTS de_practice.payments (
    order_id INT PRIMARY KEY REFERENCES de_practice.orders(order_id),
    amount INT,
    status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS de_practice.refunds (
    refund_id INT PRIMARY KEY,
    order_id INT REFERENCES de_practice.orders(order_id),
    refund_amount INT
);

INSERT INTO de_practice.orders (order_id, service_name, customer_id, ordered_at) VALUES
    (101, 'idus', 1, '2026-10-13'),
    (102, 'idus', 2, '2026-10-13'),
    (103, '10x10', 1, '2026-10-13'),
    (104, 'tumblbug', 3, '2026-10-13'),
    (105, 'idus', 2, '2026-10-14'),
    (106, '10x10', 4, '2026-10-14'),
    (107, 'tumblbug', 1, '2026-10-14'),
    (108, 'idus', 5, '2026-10-14')
ON CONFLICT DO NOTHING;

INSERT INTO de_practice.payments (order_id, amount, status) VALUES
    (101, 30000, 'PAID'),
    (102, 50000, 'PAID'),
    (103, 40000, 'PAID'),
    (104, 70000, 'FAILED'),
    (105, 60000, 'PAID'),
    (106, 20000, 'PAID'),
    (107, 90000, 'PAID'),
    (108, 15000, 'PAID')
ON CONFLICT DO NOTHING;

INSERT INTO de_practice.refunds (refund_id, order_id, refund_amount) VALUES
    (1, 102, 20000),
    (2, 102, 5000),
    (3, 106, 20000),
    (4, 107, 10000)
ON CONFLICT DO NOTHING;
