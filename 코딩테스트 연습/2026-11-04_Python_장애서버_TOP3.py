# 2026-11-04
# 문제: 서버별 FAIL 횟수를 계산하고 FAIL이 많은 서버 TOP 3를 반환한다.
# 동률이면 서버 이름 오름차순.
# 핵심: 집계 + 다중 정렬 기준

logs = [
    {"server": "A", "status": "FAIL"},
    {"server": "B", "status": "FAIL"},
    {"server": "A", "status": "OK"},
    {"server": "C", "status": "FAIL"},
    {"server": "B", "status": "FAIL"},
    {"server": "D", "status": "OK"},
    {"server": "C", "status": "FAIL"},
    {"server": "B", "status": "OK"},
    {"server": "A", "status": "FAIL"},
    {"server": "D", "status": "FAIL"},
    {"server": "C", "status": "OK"},
    {"server": "B", "status": "FAIL"},
]


# ============================================================
# 1. 직접 작성한 풀이
# ============================================================

def top_failed_servers_first(logs):
    top_k = {}
    result = []

    for i in logs:
        cu_k = i["server"]
        cu_v = i["status"]

        if cu_k not in top_k:
            top_k[cu_k] = {
                "OK": 0,
                "FAIL": 0
            }

        top_k[cu_k][cu_v] += 1

    new_top_k = dict(
        sorted(
            top_k.items(),
            key=lambda x: (-x[1]["FAIL"], x[0])
        )
    )

    for key in new_top_k:
        if new_top_k[key]["FAIL"] == 0:
            pass
        else:
            if new_top_k[key] not in result and len(result) != 3:
                result.append([key, new_top_k[key]["FAIL"]])

    return result


# 결과는 정답:
# [["B", 3], ["A", 2], ["C", 2]]


# ============================================================
# 2. 잘한 점
# ============================================================

# 다중 정렬 기준을 정확히 잡았다.
#
# key=lambda x: (-x[1]["FAIL"], x[0])
#
# - FAIL 횟수는 내림차순
# - 서버명은 오름차순


# ============================================================
# 3. 개선할 부분
# ============================================================

# new_top_k[key]는
# {"OK": 1, "FAIL": 2}
# 같은 dict다.
#
# result 안에는
# ["A", 2]
# 같은 list가 들어간다.
#
# 따라서
# new_top_k[key] not in result
# 는 형태 자체가 달라 사실상 불필요한 조건이었다.
#
# 또한 결과에는 FAIL 횟수만 필요하므로
# 처음부터 OK/FAIL을 모두 저장하지 않고
# server -> fail_count만 저장하는 방식으로 단순화할 수도 있다.


# ============================================================
# 4. 정리한 풀이
# ============================================================

def top_failed_servers(logs):
    fail_count = {}

    for log in logs:
        if log["status"] != "FAIL":
            continue

        server = log["server"]

        if server not in fail_count:
            fail_count[server] = 0

        fail_count[server] += 1

    ranked = sorted(
        fail_count.items(),
        key=lambda x: (-x[1], x[0])
    )

    result = []

    for server, count in ranked:
        if len(result) == 3:
            break

        result.append([server, count])

    return result


print(top_failed_servers(logs))


# ============================================================
# 5. 시간복잡도
# ============================================================

# N = 로그 수
# K = FAIL이 발생한 서버 수
#
# 집계 O(N)
# 정렬 O(K log K)
# 전체 O(N + K log K)


# ============================================================
# 6. 기억할 패턴
# ============================================================

# 여러 정렬 기준:
#
# sorted(data, key=lambda x: (-숫자, 문자열))
#
# 숫자 내림차순 + 문자열 오름차순
