# 2026-11-19 Python 코딩테스트 — 10분 이내 로그인 실패 탐지
#
# 학습 판정: [실패 — 독립 해결 실패 / AI 도움 비중 매우 높음]
#
# 정확한 기록:
# - 최종 코드는 정답이지만, 독립적으로 문제를 해결한 것이 아니다.
# - 사용자별 실패 시각을 dict + deque로 관리하라는 접근은 AI가 제공했다.
# - 오래된 실패 시각을 제거하는 while 조건과 popleft() 구현을 AI가 직접 알려줬다.
# - 사용자는 특히 그 while이 각 단계에서 어떻게 동작하는지 충분히 이해하지 못했다.
# - 10분 경계 조건도 처음에는 잘못 답했으며, 설명 후에는 수정했다.
# - 매 로그 처리 직후 탐지하도록 바꾸라는 수정 힌트도 AI가 제공했다.
# - 따라서 '정답 처리'가 아니라 '도움받아 코드 완성, 개념 복습 필요'로 기록한다.
#
# [문제]
# 로그는 minute 오름차순이며, 한 사용자가 10분 이내(정확히 10분 차이 포함)에
# FAIL 3회 이상이면 탐지한다.
# SUCCESS는 실패로 세지 않고 이전 기록도 초기화하지 않는다.
# 사용자는 한 번만 포함하고, 이름 오름차순 리스트로 반환한다.
#
# 기대값: ['kim', 'park']


import collections

logs = [
    {"minute": 1, "user": "kim", "status": "FAIL"},
    {"minute": 2, "user": "lee", "status": "FAIL"},
    {"minute": 6, "user": "kim", "status": "FAIL"},
    {"minute": 10, "user": "park", "status": "FAIL"},
    {"minute": 11, "user": "kim", "status": "FAIL"},
    {"minute": 12, "user": "lee", "status": "FAIL"},
    {"minute": 13, "user": "lee", "status": "FAIL"},
    {"minute": 14, "user": "lee", "status": "SUCCESS"},
    {"minute": 19, "user": "park", "status": "FAIL"},
    {"minute": 20, "user": "park", "status": "FAIL"}
]


# [최초 시도: 사용자 이름 자체를 deque에 보관하려고 함]
#
# def detect_suspicious_logins(logs):
#     deq = collections.deque()
#
#     if len(logs) == 0:
#         return []
#     else:
#         for start in logs:
#             if start['user'] not in deq:
#                 deq.append(start['user'])
#
#                 current = deq.popleft()
#
#                 for current  # 여기서 막혀 더 작성하지 못함
#
# 오류/막힘:
# - 필요한 정보는 '사용자 이름의 탐색 순서'가 아니라 '사용자별 FAIL 시각'이다.
# - BFS에서 Queue를 사용하던 감각으로 접근했지만 이번 문제는 그래프 탐색이 아니다.


# [중간 시도: 사용자별 시각은 저장했지만 별도의 두 번째 반복문으로 처리]
#
# for log in logs:
#     ...  # 로그 순회, FAIL만 저장
#     if user not in fail_times:
#         fail_times[user] = collections.deque()
#     fail_times[user].append(log['minute'])
#
# for k in fail_times:
#     result = []
#     for i in fail_times[k]:
#         result.append(i)
#         if len(result) >= 3:
#             num = result[-1] - result[0]
#             if num > 10:
#                 fail_times[k].pop()
#
# 오류/막힘:
# - result를 리스트로 덮어써 사용자 이름을 담아야 하는 집합이 사라졌다.
# - pop()은 최신 기록을 제거한다. 오래된 기록은 popleft()로 제거해야 한다.
# - deque를 반복문으로 순회하며 변경하려 했다.
# - 시각별 슬라이딩 윈도우를 유지해야 하는데 최종 집계와 섞였다.


# [AI 설명을 보고 작성한 다음 단계]
# - AI가 다음 while 조건 자체를 제시했다:
#
# while fail_times[user] and minute - fail_times[user][0] > 10:
#     fail_times[user].popleft()
#
# 미이해로 기록:
# - fail_times[user][0]은 현재 Queue의 가장 오래된 FAIL 시각
# - q가 비지 않고 (현재 분 - 가장 오래된 분) > 10일 때마다 맨 앞 기록 제거
# - 여러 개가 범위를 벗어날 수 있으므로 if가 아닌 while
# - 20 - 10 == 10이면 제거하지 않는다.
#
# AI의 설명 후 경계 사례 [9, 10, 19, 20] 중 9가 제거되고
# [10, 19, 20]이 남는다고 답할 수 있었으나,
# 이를 처음부터 코드로 옮기고 실행 순서를 추적하는 능력은 재검증이 필요하다.


# [AI 도움을 받아 완성한 최종 코드 — 독립 풀이 아님]
def detect_suspicious_logins(logs):
    fail_times = {}
    result = set()

    for log in logs:
        user = log['user']
        minute = log['minute']
        status = log['status']

        if status != 'FAIL':
            continue

        if user not in fail_times:
            fail_times[user] = collections.deque()

        fail_times[user].append(minute)

        # AI가 제시한 조건을 사용. 동작 원리 복습 필요.
        while fail_times[user] and minute - fail_times[user][0] > 10:
            fail_times[user].popleft()

        # 최종 결과만 보면 안 되므로 로그가 들어올 때마다 검사한다.
        # 이 판단 시점 역시 AI의 수정 힌트를 받아 고쳤다.
        if len(fail_times[user]) >= 3:
            result.add(user)
        else:
            continue

    return sorted(result)


# 결과 확인용 테스트 — 정답이라고 해서 독립 해결은 아님
assert detect_suspicious_logins(logs) == ['kim', 'park']
assert detect_suspicious_logins([]) == []
assert detect_suspicious_logins([
    {"minute": 1, "user": "kim", "status": "FAIL"},
    {"minute": 2, "user": "kim", "status": "FAIL"},
    {"minute": 3, "user": "kim", "status": "FAIL"},
    {"minute": 30, "user": "kim", "status": "FAIL"}
]) == ['kim']
assert detect_suspicious_logins([
    {"minute": 10, "user": "park", "status": "FAIL"},
    {"minute": 19, "user": "park", "status": "FAIL"},
    {"minute": 20, "user": "park", "status": "FAIL"}
]) == ['park']


# [손으로 추적할 예시 — 정답 코드 작성 전 해석 능력부터 연습할 것]
# lee의 FAIL 시각이 차례로 2, 12, 13일 때:
# minute=2:  q=[2]        -> 2-2=0,   유지
# minute=12: q=[2,12]     -> 12-2=10, 유지
# minute=13: q=[2,12,13]  -> 13-2=11, 2 제거 -> q=[12,13]
#
# 별도의 예:
# minute=20, q=[9,10,19,20]
# 20-9=11 -> 9 제거
# 20-10=10 -> 10 유지, while 종료
# 최종 q=[10,19,20]


# [미해결 과제 / 다음 복습 기준]
# 1. 코드를 실행하기 전에 각 줄 뒤 dict/deque/result가 어떻게 변하는지
#    5~6개 로그에 대해 손으로 추적한다.
# 2. while에서 현재 시각, q[0], 조건의 True/False를 직접 표로 쓴다.
# 3. 현재 입력이 아니라 과거에 이미 탐지됐던 사용자를 언제 result에 넣어야 하는지
#    검사 시점을 스스로 설명한다.
# 4. 다음번에는 코드 골격 없이 작은 예제로 같은 구조를 직접 작성한다.
#
# [진단]
# 문법만의 문제가 아니라, 반복문을 한 번 실행할 때 자료구조가 어떻게 변하는지
# 상태를 예측하고, 그 상태를 기준으로 조건과 검사 시점을 설계하는 과정이 약하다.
# BFS/DFS 숙련 부족과 일부 연결되지만 슬라이딩 윈도우 자체는 별개 유형이다.
#
# 예상 시간복잡도: O(N + K log K)
# N=로그 수, K=탐지 사용자 수; 각 FAIL 시각은 최대 1번 append/popleft된다.
# 이는 해설 정리이며 사용자 스스로 도출한 복잡도 분석은 아니다.


if __name__ == "__main__":
    print(detect_suspicious_logins(logs))
