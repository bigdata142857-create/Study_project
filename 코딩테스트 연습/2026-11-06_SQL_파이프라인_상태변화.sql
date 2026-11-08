-- 2026-11-06 SQL - 파이프라인 상태 변화 찾기
--
-- 문제
-- pipeline_runs에서 같은 pipeline의 바로 이전 실행 상태를 구하고,
-- 이전 상태와 현재 상태가 달라진 행만 출력한다.
--
-- 핵심
-- 1. 현재 상태는 현재 행의 status 자체다.
-- 2. 이전 상태는 LAG()로 가져온다.
-- 3. 같은 pipeline 안에서 비교해야 하므로 PARTITION BY pipeline_id.
-- 4. 실행 순서는 started_at 기준.
-- 5. 상태가 달라진 행만 바깥 WHERE에서 필터링한다.


-- 처음 시도에서의 실수
-- 1) ORDER BY 오타
-- 2) status AS current_status 문법에서 불필요한 쉼표
-- 3) 집계 문제가 아닌데 GROUP BY를 추가함
--
-- 잘못된 형태 예:
-- GROUP BY pipeline_id, run_id
--
-- 이 문제는 각 실행 행을 그대로 유지하면서 이전 행과 비교하는 문제라
-- COUNT/SUM 같은 집계가 없고 GROUP BY도 필요 없다.


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


-- 기억할 패턴
-- 이전 행 값        -> LAG()
-- 같은 그룹 내부    -> PARTITION BY
-- 행의 순서 정의     -> ORDER BY
-- Window 결과 필터링 -> CTE/Subquery 바깥 WHERE
-- 단순 행 비교 문제   -> GROUP BY 불필요
