-- 2026-11-18 SQL 코딩테스트 — 중복 메타데이터 정리 대상 탐지
--
-- [문제]
-- customer_metadata(record_id, customer_id, metadata_key, metadata_value, updated_at)
--
-- 같은 customer_id와 metadata_key를 동일한 항목으로 간주한다.
-- 각 항목에서는 updated_at이 가장 최근인 기록 한 건만 유지한다.
-- updated_at이 같으면 record_id가 더 큰 행을 유지한다.
-- 유지할 최신 행을 제외하고 '정리 대상'인 과거 중복 행만 조회한다.
-- DELETE하지 않는다.
--
-- 출력: customer_id, metadata_key, record_id, updated_at
-- 정렬: customer_id ASC, metadata_key ASC, record_id ASC
--
-- [예상 출력 record_id] 201, 204, 207, 208
-- customer_id=20의 phone은 updated_at이 동일하므로 record_id 205를 유지,
-- 204가 정리 대상이다.


-- 1. 최초 시도 (오류를 기록한 코드: 그대로 실행하면 안 됨)
--
-- WITH customer AS(
-- SELECT customer_id, metadata_key, record_id, updated_at, metadata_key,
-- ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY updated_at DESC, record_id DESC) AS rn
-- FROM customer_metadata)
--
-- SELECT customer_id, metadata_key, record_id, updated_at
-- FROM customer
-- WHERE rn = 1
-- ORDER BY `customer_id ASC`, `metadata_key ASC`, `record_id ASC`;
--
-- 오류 및 개선점
-- - metadata_key를 SELECT에 중복 기재함.
-- - PARTITION BY customer_id만 사용하면 동일 고객의 phone/email이 섞임.
--   -> customer_id, metadata_key 두 컬럼으로 그룹을 나눠야 한다.
-- - rn = 1은 '유지할 최신 행'을 조회하는 조건.
--   이번 문제는 '정리할 과거 중복 행'을 요구하므로 rn > 1이 맞다.
-- - PostgreSQL에서는 ORDER BY에 백틱(`)으로 컬럼과 방향을 감싸지 않는다.
-- - 요구사항의 '최신 기록을 유지'와 '과거 기록을 출력'을 처음에 혼동했음.


-- 2. 최종 정답 — 직접 작성한 코드
WITH customer AS (
    SELECT
        customer_id,
        metadata_key,
        record_id,
        updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id, metadata_key
            ORDER BY updated_at DESC, record_id DESC
        ) AS rn
    FROM customer_metadata
)
SELECT
    customer_id,
    metadata_key,
    record_id,
    updated_at
FROM customer
WHERE rn > 1
ORDER BY customer_id, metadata_key, record_id;


-- 3. 결과 이해
--
-- customer_id | metadata_key | record_id | updated_at
-- ------------+--------------+-----------+-----------------
-- 10          | phone        | 201       | 2026-11-15 09:00
-- 20          | phone        | 204       | 2026-11-15 12:00
-- 30          | phone        | 207       | 2026-11-16 11:00
-- 30          | phone        | 208       | 2026-11-17 10:00
--
-- PARTITION BY: '어떤 레코드끼리 중복인가?'를 정의한다.
-- ORDER BY: 그 중 '어떤 기록을 유지할 것인가?'를 정한다.
-- ROW_NUMBER: 각 항목의 최신 행에 rn = 1을 부여한다.
-- WHERE rn > 1: 최신 행을 제외한 중복 후보를 조회한다.
--
-- [중요 구분]
-- WHERE rn = 1  -> 유지할 최신 데이터 조회
-- WHERE rn > 1  -> 정리 대상인 과거 중복 데이터 조회
--
-- 실제 삭제 전에는 출력 결과와 중복 기준을 반드시 검증해야 한다.
-- 이 쿼리는 조회 전용이며 데이터 변경은 하지 않는다.
--
-- 참고: WINDOW 정렬과 이후 조회 비용은 인덱스/데이터량/실행계획에 따라 달라진다.
