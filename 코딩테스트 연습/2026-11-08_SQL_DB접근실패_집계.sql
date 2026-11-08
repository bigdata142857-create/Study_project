-- 2026-11-08 SQL - DB 접근 실패 사용자 집계
-- 핵심: GROUP BY + 조건부 집계 + HAVING

SELECT
    user_id,
    COUNT(log_id) AS total_access,
    SUM(CASE WHEN result = 'DENY' THEN 1 ELSE 0 END) AS deny_count
FROM access_logs
GROUP BY user_id
HAVING SUM(CASE WHEN result = 'DENY' THEN 1 ELSE 0 END) >= 2
ORDER BY user_id ASC;

-- 기억할 패턴
-- 전체 건수 -> COUNT()
-- 특정 상태 건수 -> SUM(CASE WHEN ... THEN 1 ELSE 0 END)
-- 집계 결과 조건 -> HAVING
