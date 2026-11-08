# 2026-11-08 Python - 연속 로그인 실패 탐지
# 핵심: 사용자별 연속 상태 관리

logs = [
    {"user": "kim",  "status": "FAIL"},
    {"user": "kim",  "status": "FAIL"},
    {"user": "lee",  "status": "SUCCESS"},
    {"user": "kim",  "status": "FAIL"},
    {"user": "kim",  "status": "SUCCESS"},
    {"user": "lee",  "status": "FAIL"},
    {"user": "lee",  "status": "FAIL"},
    {"user": "lee",  "status": "FAIL"},
    {"user": "park", "status": "FAIL"},
]

def detect_brute_force(logs):
    result = []
    m_logs = {}

    for log in logs:
        user = log["user"]
        status = log["status"]

        if user not in m_logs:
            m_logs[user] = {"FAIL": 0, "SUCCESS": 0}

        m_logs[user][status] += 1

        if m_logs[user][status] >= 3 and user not in result:
            result.append(user)

        if status == "SUCCESS":
            m_logs.pop(user)

    result.sort()
    return result

print(detect_brute_force(logs))

# 첫 시도에서의 핵심 실수
# - m_logs[user]은 dict인데 result에는 문자열 user가 들어가므로 서로 비교하면 안 됨
# - sorted(result)는 원본을 바꾸지 않음. result = sorted(result) 또는 result.sort() 필요

# 더 단순한 방향
# 이번 문제에서는 SUCCESS 횟수 자체는 필요하지 않고 연속 FAIL 횟수만 저장하면 됨.

# 기억할 패턴
# FAIL -> 연속 횟수 +1
# SUCCESS -> 해당 사용자의 연속 상태 초기화
# 한 번 조건을 만족한 사용자는 중복 추가하지 않기
