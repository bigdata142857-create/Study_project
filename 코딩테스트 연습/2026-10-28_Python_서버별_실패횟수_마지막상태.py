# 2026-10-28
# 문제: 서버별 FAIL 횟수와 마지막 상태를 구한다.
# 핵심: 초기화와 공통 갱신 분리 / 조건부 누적

logs = [
    {"server": "A", "status": "OK",   "time": 10},
    {"server": "B", "status": "FAIL", "time": 12},
    {"server": "A", "status": "FAIL", "time": 15},
    {"server": "C", "status": "OK",   "time": 11},
    {"server": "B", "status": "OK",   "time": 18},
    {"server": "A", "status": "FAIL", "time": 20},
    {"server": "B", "status": "FAIL", "time": 22},
]

# time 순서는 정렬되어 있다고 가정한다.
#
# 목표 결과
# {
#     "A": {"fail_count": 2, "last_status": "FAIL"},
#     "B": {"fail_count": 2, "last_status": "FAIL"},
#     "C": {"fail_count": 0, "last_status": "OK"}
# }


# ============================================================
# 1. 내가 직접 완성한 풀이
# ============================================================

def summarize_servers_first(logs):
    group = {}

    for key in logs:
        cu_server = key["server"]
        cu_status = key["status"]

        if cu_server not in group:
            group[cu_server] = {
                "fail_count": 0,
                "last_status": cu_status
            }

            if group[cu_server]["last_status"] == "FAIL":
                group[cu_server]["fail_count"] += 1

        else:
            group[cu_server]["last_status"] = cu_status

            if group[cu_server]["last_status"] == "FAIL":
                group[cu_server]["fail_count"] += 1

    return group


print(summarize_servers_first(logs))


# ============================================================
# 2. 이 풀이는 정답인가?
# ============================================================

# 정답이다.
#
# 새로운 서버:
# - 구조 생성
# - last_status에 현재 상태 저장
# - FAIL이면 fail_count +1
#
# 기존 서버:
# - last_status를 현재 상태로 갱신
# - FAIL이면 fail_count +1
#
# 한 번의 순회로 원하는 결과를 만든다.


# ============================================================
# 3. 개선할 수 있는 부분
# ============================================================

# 아래 로직이 if / else 양쪽에 반복된다.
#
# if ... == "FAIL":
#     fail_count += 1
#
# 그리고 현재 상태는 이미 cu_status에 있으므로
# last_status에 넣은 값을 다시 읽어서 비교할 필요가 없다.
#
# "처음 등장했을 때만 해야 하는 일"과
# "모든 로그에서 해야 하는 일"을 분리하면 더 간단해진다.


# ============================================================
# 4. 정리한 풀이
# ============================================================

def summarize_servers(logs):
    group = {}

    for key in logs:
        cu_server = key["server"]
        cu_status = key["status"]

        if cu_server not in group:
            group[cu_server] = {
                "fail_count": 0,
                "last_status": ""
            }

        # 모든 로그에서 공통으로 수행
        group[cu_server]["last_status"] = cu_status

        # FAIL인 경우에만 누적
        if cu_status == "FAIL":
            group[cu_server]["fail_count"] += 1

    return group


print(summarize_servers(logs))


# ============================================================
# 5. 시간복잡도
# ============================================================

# N = 로그 개수
#
# for문 1회 -> O(N)
# dict 조회/갱신 평균 O(1)
#
# 전체 시간복잡도 O(N)
# 서버 종류가 K개라면 공간복잡도 O(K)


# ============================================================
# 6. 기억할 패턴
# ============================================================

# 1) 처음 등장했을 때만 자료구조를 초기화한다.
# 2) 매 행마다 해야 하는 갱신은 if 바깥으로 뺀다.
# 3) 특정 조건일 때만 누적한다.
#
# if key not in result:
#     result[key] = 초기값
#
# result[key]["항상 갱신"] = 현재값
#
# if 조건:
#     result[key]["누적값"] += 1
