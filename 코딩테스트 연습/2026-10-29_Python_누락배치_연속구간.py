# 2026-10-29
# 문제: 처리되지 않은 배치 번호를 찾고 연속된 누락 구간으로 묶는다.
# 핵심: 누락값 탐색 + 연속 구간 압축

processed = [100, 101, 103, 106, 107, 110]
start = 100
end = 110

# 목표 결과
# [
#     [102, 102],
#     [104, 105],
#     [108, 109]
# ]


# ============================================================
# 1. 처음 접근
# ============================================================

def find_missing_ranges_first(processed, start, end):
    full_range = []
    missing_range = []
    result = []

    for i in range(start, end + 1):
        full_range.append(i)

    for num in full_range:
        if num not in processed:
            missing_range.append(num)

    print(missing_range)


# 여기까지는 누락값:
# [102, 104, 105, 108, 109]
# 를 찾는 데 성공했다.


# ============================================================
# 2. 막혔던 부분
# ============================================================

# 누락값을 찾은 뒤
# [102, 102], [104, 105], [108, 109]
# 처럼 "연속된 구간"으로 묶는 방법에서 막혔다.
#
# 처음에는 현재 숫자에서 +1을 하거나 extend를 쓰는 방식을 고민했지만,
# 그렇게 하면 구간 경계를 유지하기 어렵다.
#
# append([start, end])를 써야 한 구간이 하나의 리스트로 유지된다.


# ============================================================
# 3. 핵심 아이디어
# ============================================================

# start   : 현재 연속 구간의 시작값
# prev    : 바로 직전에 본 누락값
# current : 현재 보고 있는 누락값
#
# current == prev + 1
# -> 같은 구간
#
# current != prev + 1
# -> 이전 구간 종료
# -> [start, prev] 저장
# -> 새 구간 시작


# ============================================================
# 4. 최종 풀이
# ============================================================

def find_missing_ranges(processed, start, end):
    processed = sorted(processed)

    full_range = []
    missing_range = []
    result = []

    for i in range(start, end + 1):
        full_range.append(i)

    for num in full_range:
        if num not in processed:
            missing_range.append(num)

    # 누락값이 없으면 바로 종료
    if not missing_range:
        return []

    start = missing_range[0]
    prev = missing_range[0]

    for key in range(1, len(missing_range)):
        current = missing_range[key]

        if current == prev + 1:
            prev = current
        else:
            result.append([start, prev])
            start = current
            prev = current

    # 마지막 구간은 뒤에서 끊어줄 다음 숫자가 없으므로
    # 반복문 종료 후 직접 추가한다.
    result.append([start, prev])

    return result


print(find_missing_ranges(processed, start, end))


# ============================================================
# 5. 시간복잡도
# ============================================================

# 현재 풀이에서
# num not in processed 는 list 탐색이라 O(N)이다.
# 범위 길이를 M이라고 하면 최악에는 O(M * N).
#
# 추후 최적화 시 processed를 set으로 바꾸면
# membership 검사가 평균 O(1)이 되어 더 효율적이다.


# ============================================================
# 6. 기억할 패턴
# ============================================================

# 연속 구간 묶기:
#
# start = values[0]
# prev = values[0]
#
# for current in values[1:]:
#     if current == prev + 1:
#         prev = current
#     else:
#         result.append([start, prev])
#         start = current
#         prev = current
#
# result.append([start, prev])
