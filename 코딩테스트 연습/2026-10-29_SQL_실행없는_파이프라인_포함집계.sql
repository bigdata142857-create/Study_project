-- 2026-10-29
-- 문제: 실행 이력이 없는 파이프라인도 포함해서
-- total_runs / success_count / fail_count를 집계한다.
-- 핵심: LEFT JOIN + 조건부 집계

-- ============================================================
-- 1. 처음 시도
-- ============================================================

SELECT
    P.pipeline_id,
    P.pipeline_name,
    COUNT(R.pipeline_id) AS total_runs,
    CASE WHEN R.status = 'SUCCESS' THEN 1 ELSE 0 AS sucess_count,
    CASE WHEN R.status = 'FAIL' THEN 1 ELSE 0 AS fail_count
FROM pipelines P
LEFT JOIN pipline_runs R
    ON P.pipline_id = R.pipeline_id
ORDER BY pipeline_id ASC;


-- ============================================================
-- 2. 잘한 점
-- ============================================================

-- 실행 이력이 없는 vector_sync도 결과에 남겨야 하므로
-- LEFT JOIN을 선택한 것은 정확했다.


-- ============================================================
-- 3. 수정이 필요했던 부분
-- ============================================================

-- (1) CASE는 END로 닫아야 한다.
--
-- CASE WHEN ... THEN 1 ELSE 0 END
--
-- (2) 성공/실패 "횟수"를 구해야 하므로 CASE 결과를 집계해야 한다.
--
-- (3) COUNT(CASE WHEN ... THEN 1 ELSE 0 END)는
-- 0도 NULL이 아니므로 모든 행을 세게 된다.
--
-- 따라서 둘 중 하나:
--
-- COUNT(CASE WHEN 조건 THEN 1 END)
-- SUM(CASE WHEN 조건 THEN 1 ELSE 0 END)
--
-- (4) 집계 문제이므로 GROUP BY가 필요하다.
-- (5) pipline_runs / pipline_id 오타 수정 필요.


-- ============================================================
-- 4. 최종 풀이
-- ============================================================

SELECT
    P.pipeline_id,
    P.pipeline_name,
    COUNT(R.pipeline_id) AS total_runs,
    SUM(CASE WHEN R.status = 'SUCCESS' THEN 1 ELSE 0 END) AS success_count,
    SUM(CASE WHEN R.status = 'FAIL' THEN 1 ELSE 0 END) AS fail_count
FROM pipelines P
LEFT JOIN pipeline_runs R
    ON P.pipeline_id = R.pipeline_id
GROUP BY
    P.pipeline_id,
    P.pipeline_name
ORDER BY
    P.pipeline_id ASC;


-- ============================================================
-- 5. 기억할 패턴
-- ============================================================

-- 모든 기준 행을 남겨야 한다:
-- LEFT JOIN
--
-- 실행 이력 수:
-- COUNT(R.pipeline_id)
--
-- 조건부 개수:
-- SUM(CASE WHEN 조건 THEN 1 ELSE 0 END)
--
-- COUNT는 NULL이 아닌 값의 개수를 센다.
-- SUM은 실제 숫자 합계를 구한다.
