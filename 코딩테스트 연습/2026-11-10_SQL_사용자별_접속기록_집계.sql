-- 2026-11-10 SQL - 사용자별 접속 기록 집계
-- 문제 제시: 11/9 SQL 학습 문제, 풀이 및 수정: 11/10
--
-- db_users(user_id, user_name)
-- login_logs(log_id, user_id, status, accessed_at)
--
-- 모든 사용자에 대해:
-- user_name / total_logins / fail_count / last_access
-- 접속 이력이 없는 사용자도 포함하고 이름 오름차순 정렬.
--
-- 예시 기대 결과
-- choi | 0 | 0 | NULL
-- kim  | 3 | 1 | 2026-11-09 10:00
-- lee  | 2 | 2 | 2026-11-09 09:30
-- park | 1 | 0 | 2026-11-09 09:40


-- 1. 처음 제출한 풀이 (문법 및 집계 단계 문제로 실행 불가)
-- 원문을 오류 복습용으로 주석에 보존
--
-- WITH login AS (
-- SELECT user_id, log_id,
-- ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY accessed_at DESC) AS rn,
-- SUM(CASE WHEN status = 'FAIL' 1 ELSE 0 END) AS fail_count,
-- COUNT(STATUS) AS total_logins, accessed_at
-- FROM login_logs
-- )
--
-- SELECT U.user_id AS user_name, L.total_logins, L.fail_count, L.accessed_at AS last_access
-- FROM db_users U
-- LEFT JOIN login L
-- ON U.user_id = L.user_id
-- GROUP BY U.user_id
-- HAVING L.rn =1
-- ORDER BY U.user_id ASC;
--
-- 문제점
-- - CASE WHEN에서 THEN 빠짐.
-- - ROW_NUMBER()로 가장 최근 1행을 선택할 필요가 없었다.
-- - 집계 함수와 비집계 컬럼을 함께 쓰면서 적절한 GROUP BY가 없었다.
-- - HAVING rn = 1은 잘못된 조건이며 접속 기록 없는 사용자도 배제할 수 있다.
-- - user_id AS user_name은 실제 사용자 이름을 선택한 것이 아니다.
-- - 요구사항은 모든 사용자에 대한 집계와 최근 '시간'이므로 MAX(accessed_at)을 사용하면 됨.


-- 2. 힌트 후 직접 수정한 풀이
-- 논리와 집계는 올바름. ORDER BY만 user_id에서 user_name으로 변경 필요.
--
-- SELECT U.user_name,
-- COUNT(L.status) AS total_logins,
-- SUM(CASE WHEN L.status = 'FAIL' THEN 1 ELSE 0 END) AS fail_count,
-- MAX(L.accessed_at) AS last_access
-- FROM db_users U
-- LEFT JOIN login_logs L
-- ON U.user_id = L.user_id
-- GROUP BY U.user_id
-- ORDER BY U.user_id ASC;
--
-- 참고: PostgreSQL에서 U.user_id가 PRIMARY KEY라면
-- GROUP BY U.user_id만으로 U.user_name을 SELECT할 수 있다.
-- 이 연습에서는 PK 여부에 덜 의존하도록 두 컬럼을 그룹에 포함한다.


-- 3. 요구사항을 모두 만족하도록 정리한 최종 풀이
SELECT
    U.user_name,
    COUNT(L.log_id) AS total_logins,
    SUM(CASE WHEN L.status = 'FAIL' THEN 1 ELSE 0 END) AS fail_count,
    MAX(L.accessed_at) AS last_access
FROM db_users U
LEFT JOIN login_logs L
    ON U.user_id = L.user_id
GROUP BY U.user_id, U.user_name
ORDER BY U.user_name ASC;


-- 기억할 패턴
-- 모든 기준 테이블 행 보존  -> LEFT JOIN
-- 전체 접속 횟수            -> COUNT(L.log_id) (COUNT(*) 사용 X)
-- 조건부 FAIL 횟수          -> SUM(CASE WHEN ... THEN 1 ELSE 0 END)
-- 최근 접속 시각            -> MAX(accessed_at)
-- 사용자별 집계             -> GROUP BY
-- 모든 사용자 필요          -> HAVING으로 일부 제거하지 않음
-- 사용자명 오름차순         -> ORDER BY U.user_name ASC
--
-- DISTINCT/ROW_NUMBER는 최신 '행' 자체가 필요할 때 검토한다.
-- 최신 '시각'만 필요하다면 MAX()로 충분하다.
--
-- 복잡도 메모
-- DB 엔진의 실행 계획, 조인·집계 방식 및 인덱스 유무에 따라 달라진다.
