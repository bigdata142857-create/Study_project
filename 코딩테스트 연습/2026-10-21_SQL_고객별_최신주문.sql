-- 2026-10-21
-- 문제: 고객별 가장 최근 주문 1건을 조회한다.
-- 핵심: Window Function / ROW_NUMBER()

-- ============================================================
-- 1. 처음 시도
-- ============================================================

WITH order AS (
    SELECT
        customer_id,
        order_id,
        amount,
        ordered_at,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY ordered_at DESC
        ) AS rn
    FROM orders
)

SELECT
    customer_id,
    order_id,
    amount,
    ordered_at
FROM order
WHERE rn = 1
ORDER BY customer_id ASC;


-- ============================================================
-- 2. 왜 정답이 아니었는가
-- ============================================================

-- 문제는 "고객별 최신 주문"을 찾는 것이므로
-- 각 customer_id 안에서 ordered_at을 비교해야 한다.
--
-- 그런데 처음에는 PARTITION BY order_id를 사용했다.
-- order_id가 주문마다 고유하다면 각 파티션에 행이 1개뿐이므로
-- 모든 행의 rn이 1이 되어 버린다.
--
-- 기억할 질문:
-- "무엇마다 1등을 한 개씩 뽑으려고 하는가?"
-- -> 고객마다 1개를 뽑으므로 PARTITION BY customer_id


-- ============================================================
-- 3. 수정한 풀이
-- ============================================================

WITH recent_orders AS (
    SELECT
        customer_id,
        order_id,
        amount,
        ordered_at,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY ordered_at DESC
        ) AS rn
    FROM orders
)

SELECT
    customer_id,
    order_id,
    amount,
    ordered_at
FROM recent_orders
WHERE rn = 1
ORDER BY customer_id ASC;


-- ============================================================
-- 4. 배운 점
-- ============================================================

-- 1) ROW_NUMBER()를 떠올리는 것만으로는 부족하다.
-- 2) PARTITION BY는 "그룹을 나누는 기준"이다.
-- 3) 최신 행 전체를 가져올 때 GROUP BY + MAX()만으로는
--    order_id, amount 같은 다른 컬럼을 정확히 가져오기 까다롭다.
-- 4) CTE 이름으로 order 같은 예약어 가능성이 있는 이름보다
--    recent_orders처럼 의미 있는 이름을 쓰는 편이 안전하다.
