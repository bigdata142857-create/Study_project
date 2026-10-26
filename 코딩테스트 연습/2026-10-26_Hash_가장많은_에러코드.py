# 2026-10-26
# 문제: 가장 많이 발생한 에러 코드를 반환한다.
# 동점이면 숫자가 작은 에러 코드를 반환한다.
# 핵심: Hash / 빈도수 계산 / tie-breaking

errors = [
    500,
    404,
    500,
    403,
    404,
    500,
    403,
    404,
]


# ============================================================
# 1. 내가 처음 작성한 풀이
# ============================================================

def most_common_error_first(errors):
    count = {}

    for key in errors:
        if key not in count:
            count[key] = 1
        else:
            count[key] += 1

    num = sorted(count)

    min = num[0]

    for key in num:
        if count[key] > count[min]:
            min = key
        elif count[key] == count[min] and key < min:
            min = key
        else:
            pass

    return min


print(most_common_error_first(errors))


# ============================================================
# 2. 이 풀이는 정답인가?
# ============================================================

# 정답이다.
#
# count 구조:
# {
#     500: 3,
#     404: 3,
#     403: 2
# }
#
# 다만 개선할 점이 있다.


# ============================================================
# 3. 아쉬운 점
# ============================================================

# (1) min이라는 변수명
# Python 내장 함수 min()을 덮어쓴다.
# answer, best 같은 이름이 더 좋다.
#
# (2) sorted()가 꼭 필요하지 않다.
# key 정렬 때문에 O(K log K)가 추가된다.
#
# (3) 이미 sorted(count)를 사용했다면
# 같은 횟수일 때 작은 key가 먼저 등장하므로
#
# elif count[key] == count[min] and key < min:
#
# 조건은 사실상 불필요하다.
#
# 하지만 "횟수가 같으면 작은 값"이라는 tie-breaking 사고 자체는
# 정렬 없이 푸는 최종 풀이에서 중요하다.


# ============================================================
# 4. 정렬 없이 개선한 풀이
# ============================================================

def most_common_error(errors):
    count = {}

    for error in errors:
        if error not in count:
            count[error] = 1
        else:
            count[error] += 1

    answer = None

    for error in count:
        if answer is None:
            answer = error
        elif count[error] > count[answer]:
            answer = error
        elif count[error] == count[answer] and error < answer:
            answer = error

    return answer


print(most_common_error(errors))


# ============================================================
# 5. 시간복잡도
# ============================================================

# N: 전체 에러 개수
# K: 서로 다른 에러 코드 수
#
# 첫 풀이:
# 빈도 계산 O(N)
# 정렬 O(K log K)
# 탐색 O(K)
# -> O(N + K log K)
#
# 개선 풀이:
# 빈도 계산 O(N)
# 최대 빈도 탐색 O(K)
# -> O(N + K)


# ============================================================
# 6. 기억할 패턴
# ============================================================

# 빈도수 세기 기본형:
#
# count = {}
#
# for x in data:
#     if x not in count:
#         count[x] = 1
#     else:
#         count[x] += 1
#
# dict 구조:
# 값 -> 등장 횟수
