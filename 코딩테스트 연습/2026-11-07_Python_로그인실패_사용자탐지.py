# 2026-11-07 Python - 로그인 실패 사용자 탐지

logs = [
    {"user": "kim",  "status": "FAIL"},
    {"user": "lee",  "status": "SUCCESS"},
    {"user": "kim",  "status": "FAIL"},
    {"user": "park", "status": "FAIL"},
    {"user": "kim",  "status": "SUCCESS"},
    {"user": "lee",  "status": "FAIL"},
    {"user": "kim",  "status": "FAIL"},
    {"user": "lee",  "status": "FAIL"},
    {"user": "park", "status": "SUCCESS"},
    {"user": "kim",  "status": "FAIL"},
]

# 문제
# 각 사용자별 FAIL 횟수를 계산하고,
# FAIL이 3회 이상인 사용자만 [user, fail_count] 형태로 반환한다.
#
# 정렬 조건
# 1. FAIL 횟수 내림차순
# 2. 동률이면 사용자 이름 오름차순


def find_suspicious_users(logs):
    dic_logs = {}
    result = []

    for log in logs:
        user = log["user"]
        status = log["status"]

        if user not in dic_logs:
            dic_logs[user] = {
                "FAIL": 0,
                "SUCCESS": 0
            }

        dic_logs[user][status] += 1

    for name in dic_logs:
        fail_count = dic_logs[name]["FAIL"]

        if fail_count >= 3:
            result.append([name, fail_count])

    result.sort(key=lambda x: (-x[1], x[0]))
    return result


print(find_suspicious_users(logs))


# 결과
# [['kim', 4]]
#
# 개선 포인트
# 이 문제에서는 SUCCESS 횟수는 최종 결과에 사용하지 않으므로
# FAIL만 세는 dict로 더 단순하게 구현할 수 있다.
#
# Counter도 사용할 수 있다.
#
# 기억할 패턴
# 조건에 맞는 로그만 집계 -> dict / Counter
# 다중 정렬              -> key=lambda x: (-x[1], x[0])
