-- 2026-11-06 SQL - 파이프라인 상태 변경 탐지
-- 핵심: LAG + PARTITION BY + ORDER BY + CTE

WITH pipe AS (
    SELECT
        pipeline_id,
        run_id,
        LAG(status) OVER (
            PARTITION BY pipeline_id
            ORDER BY started_at
        ) AS previous_status,
        status AS current_status,
        started_at
    FROM pipeline_runs
)
SELECT
    pipeline_id,
    run_id,
    previous_status,
    current_status,
    started_at
FROM pipe
WHERE current_status <> previous_status
ORDER BY pipeline_id ASC, started_at ASC;

-- 첫 시도에서의 핵심 실수
-- - 현재 상태를 따로 구해야 한다고 생각했지만 현재 행의 status 자체가 current_status임
-- - LAG에 ORDER BY가 필요함
-- - 집계 문제가 아닌데 GROUP BY를 넣으려 함

-- 기억할 패턴
-- 이전 행 값 -> LAG()
-- 같은 그룹 안에서 비교 -> PARTITION BY
-- 비교 순서 -> ORDER BY
-- 상태가 바뀐 행만 -> WHERE current_status <> previous_status
