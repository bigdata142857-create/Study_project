-- 2026-11-15 SQL - 사용자별 가장 최근 로그인 상태 조회
--
-- 문제
-- db_users(user_id, user_name)
-- login_logs(log_id, user_id, status, accessed_at)
--
-- 모든 사용자의 가장 최근 로그인 기록 한 건의 상태와 시각을 조회한다.
-- 같은 시각이면 log_id가 더 큰 기록이 최신이다.
-- 로그인 기록이 없는 사용자도 남기고 상태는 'NO_LOG'로 출력한다.
-- user_name 오름차순 정렬.
--
-- 예상 결과
-- choi | SUCCESS | 2026-11-13 09:30
-- han  | NO_LOG  | NULL
-- kim  | SUCCESS | 2026-11-13 10:00
-- lee  | FAIL    | 2026-11-13 11:00
-- park | FAIL    | 2026-11-13 12:00


-- 1. 최초 접근 (오류 기록; 실행 불가)
--
-- WITH log AS (
--     SELECT log_id, user_id, status,
--         ROW_NUMBER() OVER(
--             PARTITION BY user_id, status
--             ORDER BY accessed_at, log_id
--         ) AS rn,
--         ROW_NUMBER() OVER(
--             PARTITION BY user_id
--             ORDER BY accessed_at, log_id
--         ) AS rnn
--     FROM login_logs
-- )
-- SELECT
-- FROM db_users D
-- LEFT JOIN log L ON D.user_id = L.user_id;
--
-- 왜 틀렸나?
-- - PARTITION BY user_id, status는 SUCCESS/FAIL을 서로 다른 그룹으로 쪼갬.
-- - 사용자별 최신 로그 1건이면 ROW_NUMBER() 하나로 충분.
-- - ASC 기본 정렬은 과거 순서부터 rn=1을 부여함.
-- - SELECT 항목 미완성.


-- 2. 수정 과정에서 나온 실수
--
-- SELECT log_id, user_id, status, accessed_at
-- ROW_NUMBER() OVER(PARTITION BY user_id, ORDER BY accessed_at DESC, log_id DESC) AS rn
--
-- - accessed_at 뒤 쉼표 누락
-- - PARTITION BY user_id 뒤 불필요한 쉼표
-- - NO_LOG를 문자열 따옴표 없이 작성함
-- - 최종 ORDER BY 사용자 이름이 누락되었던 단계가 있음


-- 3. 최종 정답 (직접 작성한 풀이)
WITH log AS (
    SELECT
        log_id,
        user_id,
        status,
        accessed_at,
        ROW_NUMBER() OVER (
            PARTITION BY user_id
            ORDER BY accessed_at DESC, log_id DESC
        ) AS rn
    FROM login_logs
)
SELECT
    D.user_name,
    COALESCE(L.status, 'NO_LOG') AS last_status,
    L.accessed_at AS last_access
FROM db_users D
LEFT JOIN log L
    ON D.user_id = L.user_id
    AND L.rn = 1
ORDER BY D.user_name;


-- 4. 쿼리 흐름
-- CTE log:
--   user_id별로 최신 시각 DESC, 동일 시각이면 log_id DESC
--   ROW_NUMBER() = 1이 해당 사용자의 최신 로그인 기록.
--
-- LEFT JOIN:
--   db_users를 기준으로 모든 사용자를 남긴다.
--   ON 절에서 L.rn = 1을 걸어 최신 로그 하나만 연결한다.
--   만약 WHERE L.rn = 1을 걸면 로그가 없는 사용자(han)는 제거될 수 있다.
--
-- COALESCE:
--   L.status가 NULL이면 'NO_LOG' 출력.
--   L.accessed_at은 NULL이면 그대로 NULL.
--
-- ORDER BY:
--   사용자 이름으로 오름차순 정렬.
--
-- 5. 이전 SQL 문제와 차이
-- 최신 접속 '시각'만 구할 때 -> MAX(accessed_at)으로 충분.
-- 최신 접속 '행의 상태와 시각'이 필요 -> ROW_NUMBER()로 한 행 선택.
--
-- 기억할 패턴
-- 최신 1건: ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ... DESC, tie_breaker DESC)
-- 기록 없는 사용자도 남김: LEFT JOIN + ON 조건에 rn = 1
-- NULL 표시: COALESCE(컬럼, '대체문자열')
--
-- 복잡도: SQL 실행계획, 인덱스 유무, 조인 전략과 정렬 방식에 따라 달라진다.
