-- 2026-10-31
-- 문제: pipeline_id별 가장 최근 실행 1건을 출력한다.
-- 핵심: ROW_NUMBER + CTE

-- ============================================================
-- 1. 첫 시도
-- ============================================================

SELECT
    pipeline_id,
    run_id,
    status,
    started_at,
    DENSE_RANK() OVER (
        PARTITION BY pipeline_id
        ORDER BY started_at DESC
    )
FROM pipeline_runs
WHERE DENSE_RANK() OVER (
    PARTITION BY pipeline_id
    ORDER BY started_at DESC
) = 1
ORDER BY pipeline_id ASC;


-- ============================================================
-- 2. 문제점
-- ============================================================

-- (1) Window Function은 같은 SELECT의 WHERE에서 바로 사용할 수 없다.
-- 먼저 CTE/서브쿼리에서 계산한 뒤 바깥에서 필터링해야 한다.
--
-- (2) DENSE_RANK는 같은 started_at이 여러 건이면
-- 여러 행이 동시에 1등이 될 수 있다.
--
-- 문제는 "정확히 1건"이므로 ROW_NUMBER가 더 적절하다.


-- ============================================================
-- 3. 두 번째 시도에서의 실수
-- ============================================================

-- CTE에서 ROW_NUMBER를 잘 만들었지만
-- 바깥에서 원본 pipeline_runs와 다시 pipeline_id로 JOIN했다.
--
-- 그러면 같은 pipeline_id의 여러 행이 다시 붙을 수 있다.
--
-- CTE 자체에 필요한 컬럼이 이미 있으므로
-- rn = 1인 행을 CTE에서 바로 조회하면 된다.


-- ============================================================
-- 4. 최종 풀이
-- ============================================================

WITH pipe AS (
    SELECT
        pipeline_id,
        run_id,
        status,
        started_at,
        ROW_NUMBER() OVER (
            PARTITION BY pipeline_id
            ORDER BY started_at DESC, run_id DESC
        ) AS rn
    FROM pipeline_runs
)

SELECT
    pipeline_id,
    run_id,
    status,
    started_at
FROM pipe
WHERE rn = 1
ORDER BY pipeline_id ASC;


-- ============================================================
-- 5. 기억할 패턴
-- ============================================================

-- 그룹별 최신 1건:
--
-- ROW_NUMBER() OVER (
--     PARTITION BY 그룹
--     ORDER BY 시간 DESC
-- )
--
-- 바깥에서 rn = 1
--
-- 동률 가능성이 있으면 run_id 같은 2차 정렬 기준을 둔다.
