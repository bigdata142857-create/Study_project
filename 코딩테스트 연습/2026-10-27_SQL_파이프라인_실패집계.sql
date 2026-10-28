-- 2026-10-27
-- 문제: 파이프라인별 실행 횟수, 성공 횟수, 실패 횟수를 집계하고
-- FAIL이 2회 이상인 파이프라인만 출력한다.
-- 핵심: JOIN + GROUP BY + 조건부 집계 + HAVING + ORDER BY

-- ============================================================
-- 1. 문제
-- ============================================================

-- pipelines
-- pipeline_id | pipeline_name
-- 1           | customer_sync
-- 2           | order_etl
-- 3           | log_batch
-- 4           | vector_sync
--
-- pipeline_runs
-- run_id | pipeline_id | status
-- 1      | 1           | SUCCESS
-- 2      | 1           | FAIL
-- 3      | 1           | FAIL
-- 4      | 2           | SUCCESS
-- 5      | 2           | SUCCESS
-- 6      | 2           | FAIL
-- 7      | 3           | FAIL
-- 8      | 3           | FAIL
-- 9      | 3           | FAIL
-- 10     | 4           | SUCCESS
--
-- 출력:
-- pipeline_id, pipeline_name, total_runs, success_count, fail_count
--
-- 조건:
-- FAIL >= 2인 파이프라인만 출력
-- fail_count DESC, pipeline_id ASC 정렬


-- ============================================================
-- 2. 내가 처음 작성한 쿼리
-- ============================================================

SELECT 
    P.pipeline_id,
    pipeline_name,
    COUNT(R.pipeline_id) AS total_runs,
    COUNT(CASE WHEN R.status = 'SUCCESS') AS success_count,
    COUNT(CASE WHEN R.status = 'FAIL') AS fail_count
FROM pipelines P
JOIN pipeline_runs R
    ON P.pipeline_id = R.pipeline_id
GROUP BY P.pipeline_id
HAVING fail_count >= 2
ORDER BY fail_count DESC, pipeline_id ASC;


-- ============================================================
-- 3. 무엇이 맞았는가
-- ============================================================

-- JOIN 방향은 맞았다.
-- GROUP BY가 필요한 집계 문제라는 판단도 맞았다.
-- 집계 결과를 조건으로 거르기 위해 WHERE가 아니라 HAVING을 선택한 것도 맞았다.
-- ORDER BY 기준도 맞았다.


-- ============================================================
-- 4. 왜 그대로는 정답이 아니었는가
-- ============================================================

-- (1) CASE WHEN 문법이 완성되지 않았다.
--
-- 처음:
-- COUNT(CASE WHEN R.status = 'SUCCESS')
--
-- 조건에 맞을 때 무엇을 반환할지 THEN이 필요하다.
--
-- COUNT(CASE WHEN R.status = 'SUCCESS' THEN 1 END)
--
-- CASE 결과:
-- SUCCESS -> 1
-- 그 외   -> NULL
--
-- COUNT는 NULL을 세지 않으므로 SUCCESS만 집계된다.


-- (2) PostgreSQL에서는 SELECT에서 만든 alias를
-- HAVING에서 바로 쓰는 방식에 의존하지 않는 것이 안전하다.
--
-- 처음:
-- HAVING fail_count >= 2
--
-- 수정:
-- HAVING COUNT(CASE WHEN R.status = 'FAIL' THEN 1 END) >= 2


-- (3) GROUP BY에는 SELECT에 그대로 출력하는 비집계 컬럼을 포함한다.
-- PostgreSQL에서는 PK의 함수적 종속성 때문에 일부 경우 허용될 수 있지만,
-- 코테에서는 명확하게 pipeline_name까지 적어두는 편이 안전하다.


-- ============================================================
-- 5. 수정한 풀이
-- ============================================================

SELECT
    P.pipeline_id,
    P.pipeline_name,
    COUNT(R.pipeline_id) AS total_runs,
    COUNT(CASE WHEN R.status = 'SUCCESS' THEN 1 END) AS success_count,
    COUNT(CASE WHEN R.status = 'FAIL' THEN 1 END) AS fail_count
FROM pipelines P
JOIN pipeline_runs R
    ON P.pipeline_id = R.pipeline_id
GROUP BY
    P.pipeline_id,
    P.pipeline_name
HAVING COUNT(CASE WHEN R.status = 'FAIL' THEN 1 END) >= 2
ORDER BY
    fail_count DESC,
    P.pipeline_id ASC;


-- ============================================================
-- 6. 기억할 패턴
-- ============================================================

-- 조건부 개수 세기:
--
-- COUNT(CASE WHEN 조건 THEN 1 END)
--
-- 또는
--
-- SUM(CASE WHEN 조건 THEN 1 ELSE 0 END)
--
-- WHERE  : GROUP BY 전에 개별 행을 거른다.
-- HAVING : GROUP BY 후 집계 결과를 거른다.
