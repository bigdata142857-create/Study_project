# 2026-10-25
# 문제: user_id별 가장 최근 timestamp를 가진 이벤트 1건만 남긴다.
# 핵심: dict의 key 설계 / 전체 레코드 갱신 / sorted() 반환값

events = [
    {"user_id": 101, "event": "login",    "timestamp": 100},
    {"user_id": 102, "event": "login",    "timestamp": 105},
    {"user_id": 101, "event": "purchase", "timestamp": 120},
    {"user_id": 103, "event": "login",    "timestamp": 110},
    {"user_id": 102, "event": "logout",   "timestamp": 130},
    {"user_id": 101, "event": "logout",   "timestamp": 125},
]


# ============================================================
# 1. 처음 막혔던 지점
# ============================================================

# 처음에는 아래처럼 딕셔너리 내부의 key까지 다시 순회하려고 했다.
#
# for i in events:
#     for key in i:
#         ...
#
# 하지만 i 자체가 이미 한 이벤트 전체를 담은 dict다.
#
# 첫 반복의 i:
# {
#     "user_id": 101,
#     "event": "login",
#     "timestamp": 100
# }
#
# 따라서 i["user_id"], i["event"], i["timestamp"]로 바로 접근할 수 있다.


# ============================================================
# 2. 첫 번째 수정 시도
# ============================================================

# latest = {}
#
# for i in events:
#     user_id = i["user_id"]
#
#     if user_id not in latest:
#         latest[user_id] = i
#     else:
#         if latest[user_id]["timestamp"] < i["timestamp"]:
#             latest[user_id]["timestamp"] = i["timestamp"]


# ============================================================
# 3. 왜 위 코드가 문제였는가
# ============================================================

# timestamp만 바꾸면 event는 과거 값이 그대로 남는다.
#
# 예:
# 기존
# {"user_id": 101, "event": "login", "timestamp": 100}
#
# timestamp만 수정
# {"user_id": 101, "event": "login", "timestamp": 120}
#
# 실제 timestamp=120 이벤트는 purchase인데
# 서로 다른 이벤트의 정보가 섞여버린다.
#
# 따라서 최신 이벤트가 발견되면 dict 전체를 교체해야 한다.


# ============================================================
# 4. 직접 완성한 코드에서의 추가 실수
# ============================================================

# def get_latest_events(events):
#     latest = {}
#
#     for i in events:
#         user_id = i["user_id"]
#         if user_id not in latest:
#             latest[user_id] = i
#         else:
#             if latest[user_id]["timestamp"] < i["timestamp"]:
#                 latest[user_id] = i
#
#     sorted(latest.items())
#
#     result = []
#
#     for j in latest.values():
#         result.append(j)
#
#     return result

# sorted()는 원본을 직접 바꾸지 않고 "정렬된 새로운 리스트"를 반환한다.
# 따라서 sorted(latest.items())의 반환값을 사용하지 않으면 정렬 효과가 없다.
#
# 현재 예제에서는 user_id가 처음 등장하는 순서가 101 -> 102 -> 103이라
# 우연히 정답처럼 보일 수 있다.


# ============================================================
# 5. 최종 풀이
# ============================================================

def get_latest_events(events):
    latest = {}

    for event in events:
        user_id = event["user_id"]

        if user_id not in latest:
            latest[user_id] = event
        elif latest[user_id]["timestamp"] < event["timestamp"]:
            latest[user_id] = event

    result = []

    for user_id in sorted(latest):
        result.append(latest[user_id])

    return result


print(get_latest_events(events))


# ============================================================
# 6. 시간복잡도
# ============================================================

# 이벤트 개수: N
# 서로 다른 사용자 수: K
#
# 최신 이벤트 저장: O(N)
# user_id 정렬: O(K log K)
# 결과 생성: O(K)
#
# 전체: O(N + K log K)


# ============================================================
# 7. 기억할 패턴
# ============================================================

# "그룹별 최신값" 문제:
#
# result = {}
#
# for item in data:
#     key = item["그룹 기준"]
#
#     if key not in result:
#         result[key] = item
#     elif result[key]["비교 기준"] < item["비교 기준"]:
#         result[key] = item
#
# 핵심:
# 그룹 기준을 dict key로 사용하고,
# 최신값이 나오면 레코드 전체를 교체한다.
