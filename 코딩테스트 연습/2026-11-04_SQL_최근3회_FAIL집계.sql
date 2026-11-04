-- 2026-11-04
-- 문제: pipeline_id별 최근 실행 3건만 보고
-- FAIL이 2회 이상인 pipeline만 출력한다.
-- 핵심: Window Function 단계와 GROUP BY 집계 단계를 분리

-- ============================================================
-- 1. 첫 시도
-- ============================================================

WITH pipe AS (
    SELECT pipeline_id,
           ROWNUMBER() OVER (
               PARTITION BY pipeline_id
               ORDER BY started_at DESC
           ) AS rn,
           SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0) AS fail_count
    FROM pipeline_runs
)

SELECT
    pipline_id,
    COUNT(status) AS recent_runs,
    fail_count
FROM pipe
WHERE rn <= 3 & fail_count >= 2
GROUP BY pipeline_id
ORDER BY pipeline_id ASC;


-- ============================================================
-- 2. 주요 문제점
-- ============================================================

-- (1) ROWNUMBER()가 아니라 ROW_NUMBER()
--
-- (2) CASE는 END로 닫아야 한다.
--
-- (3) 가장 중요한 구조 문제:
-- 최근 3건을 고르기 전에 CTE 안에서 SUM을 하면 안 된다.
--
-- 이 문제는
--
-- 1단계: 각 행에 최근 순번을 붙인다.
-- 2단계: rn <= 3인 행만 남긴다.
-- 3단계: 남은 행을 pipeline별 집계한다.
--
-- 순서로 처리해야 한다.
--
-- (4) 집계 결과 fail_count >= 2 조건은 WHERE가 아니라 HAVING.
-- (5) SQL 논리 연산자는 &가 아니라 AND.
-- (6) CTE 바깥에서 status를 집계하려면 CTE에서 status를 선택해야 한다.


-- ============================================================
-- 3. 중간에 반복했던 실수
-- ============================================================

-- CTE 안에 COUNT(status) AS recent_runs를 다시 넣었다.
--
-- 하지만 CTE의 역할은 집계가 아니라
-- "행을 유지한 채 순번을 붙이는 것"이다.
--
-- Window Function:
-- 행을 유지
--
-- GROUP BY:
-- 행을 그룹 단위로 줄임
--
-- 두 역할을 한 단계에 섞지 않는 것이 핵심.


-- ============================================================
-- 4. 최종 풀이
-- ============================================================

WITH pipe AS (
    SELECT
        pipeline_id,
        status,
        ROW_NUMBER() OVER (
            PARTITION BY pipeline_id
            ORDER BY started_at DESC, run_id DESC
        ) AS rn
    FROM pipeline_runs
)

SELECT
    pipeline_id,
    COUNT(status) AS recent_runs,
    SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) AS fail_count
FROM pipe
WHERE rn <= 3
GROUP BY pipeline_id
HAVING SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) >= 2
ORDER BY pipeline_id ASC;


-- ============================================================
-- 5. 기억할 패턴
-- ============================================================

-- "그룹별 최근 N건을 대상으로 집계"
--
-- 1. ROW_NUMBER()로 그룹별 순번 생성
-- 2. CTE 밖에서 rn <= N 필터
-- 3. GROUP BY
-- 4. 조건부 집계
-- 5. 집계 결과 조건은 HAVING
--
-- Window Function과 GROUP BY를 같은 단계에 섞지 않는다.
