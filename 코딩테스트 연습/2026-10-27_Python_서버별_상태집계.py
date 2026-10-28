# 2026-10-27
# 문제: 서버별 OK / FAIL 횟수를 집계한다.
# 핵심: dict 안의 dict / 동적 key로 누적하기

logs = [
    {"server": "A", "status": "OK"},
    {"server": "B", "status": "FAIL"},
    {"server": "A", "status": "FAIL"},
    {"server": "C", "status": "OK"},
    {"server": "B", "status": "FAIL"},
    {"server": "A", "status": "OK"},
]

# 목표 결과
# {
#     "A": {"OK": 2, "FAIL": 1},
#     "B": {"OK": 0, "FAIL": 2},
#     "C": {"OK": 1, "FAIL": 0}
# }


# ============================================================
# 1. 처음 시도
# ============================================================

# def summarize_logs(logs):
#     group = {}
#
#     for key in logs:
#         cu_server = key["server"]
#         cu_status = key["status"]
#
#         if cu_server not in group:
#             group[cu_server] = cu_status
#             group[cu_status] = 1
#
#     print(group)


# ============================================================
# 2. 왜 원하는 구조가 아니었는가
# ============================================================

# 첫 로그가 A / OK라면 위 구조는
#
# {
#     "A": "OK",
#     "OK": 1
# }
#
# 처럼 서버와 상태가 같은 레벨의 key가 된다.
#
# 하지만 문제에서 원하는 것은
#
# {
#     "A": {
#         "OK": 1,
#         "FAIL": 0
#     }
# }
#
# 처럼 "서버 -> 상태 -> 횟수"의 2단계 구조다.


# ============================================================
# 3. 두 번째 시도에서 막힌 부분
# ============================================================

# def summarize_logs(logs):
#     group = {}
#
#     for key in logs:
#         cu_server = key["server"]
#         cu_status = key["status"]
#
#         if cu_server not in group:
#             group[cu_server] = {
#                 "OK": 0,
#                 "FAIL": 0
#             }
#             group[cu_server][cu_status] += 1
#
#         elif
#             ...
#
# 여기서 "기존 서버에서 상태가 바뀌면 어떻게 하지?"
# "같은 상태가 또 나오면 어떻게 누적하지?"를 고민했다.


# ============================================================
# 4. 핵심 깨달음
# ============================================================

# 상태 변화를 따로 구분할 필요가 없다.
#
# cu_status 자체가 이미 "OK" 또는 "FAIL" 값을 가지고 있다.
#
# 예:
#
# cu_server = "A"
# cu_status = "FAIL"
#
# group[cu_server][cu_status]
# ==
# group["A"]["FAIL"]
#
# 따라서 현재 상태에 해당하는 카운트를 그냥 1 증가시키면 된다.
#
# group[cu_server][cu_status] += 1
#
# 그리고 이 누적은 "처음 등장한 서버"와 "기존 서버" 모두에서
# 공통으로 실행되어야 하므로 if 바깥에 둔다.


# ============================================================
# 5. 최종 풀이
# ============================================================

def summarize_logs(logs):
    group = {}

    for key in logs:
        cu_server = key["server"]
        cu_status = key["status"]

        if cu_server not in group:
            group[cu_server] = {
                "OK": 0,
                "FAIL": 0
            }

        group[cu_server][cu_status] += 1

    return group


print(summarize_logs(logs))


# ============================================================
# 6. 시간복잡도
# ============================================================

# N = 로그 개수
#
# 로그를 한 번 순회하고 dict 조회/갱신은 평균 O(1)
# -> 시간복잡도 O(N)
#
# 서버 수를 K라고 하면 결과 저장 공간은 O(K)


# ============================================================
# 7. 기억할 패턴
# ============================================================

# 2단계 집계:
#
# result[그룹][세부항목] += 1
#
# 예:
# errors[server][code] += 1
# sales[region][category] += amount
# users[country][status] += 1
#
# 중요한 질문:
# "이미 변수에 key 값이 들어 있는데 또 if로 나눌 필요가 있는가?"
