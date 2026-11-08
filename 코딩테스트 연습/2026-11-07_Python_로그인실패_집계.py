# 2026-11-07 Python - 사용자별 로그인 실패 집계
# 핵심: dict 집계 + 조건 필터 + 다중 정렬

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

def find_suspicious_users(logs):
    dic_logs = {}
    result = []

    for log in logs:
        user = log["user"]
        status = log["status"]

        if user not in dic_logs:
            dic_logs[user] = {"FAIL": 0, "SUCCESS": 0}

        dic_logs[user][status] += 1

    for user in dic_logs:
        fail_count = dic_logs[user]["FAIL"]
        if fail_count >= 3:
            result.append([user, fail_count])

    result.sort(key=lambda x: (-x[1], x[0]))
    return result

print(find_suspicious_users(logs))

# 더 단순한 방향
# 결과에 필요한 것이 FAIL 횟수뿐이면 SUCCESS는 저장하지 않아도 됨.
# Counter를 사용해도 됨.

# 기억할 패턴
# 조건부 집계 -> 필요한 상태만 카운트
# 정렬 -> (-count, name)
