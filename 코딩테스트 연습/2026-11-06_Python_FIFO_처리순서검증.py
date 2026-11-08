# 2026-11-06 Python - FIFO 처리 순서 검증
#
# 문제
# REQUEST가 들어온 순서대로 COMPLETE되어야 한다.
# 가장 먼저 요청된 작업이 가장 먼저 완료되는지 검증한다.
#
# 예시
logs = [
    "REQUEST A",
    "REQUEST B",
    "COMPLETE A",
    "REQUEST C",
    "COMPLETE B",
    "COMPLETE C"
]

# 잘못된 예
# ["REQUEST A", "REQUEST B", "COMPLETE B"]
# ["COMPLETE A"]
# ["REQUEST A"]


# 처음 시도에서 막힌 부분
# - REQUEST와 COMPLETE를 모두 저장하려고 했다.
# - 큐의 첫 번째 값을 어떻게 제거하는지 헷갈렸다.
#
# 수정 과정
# - REQUEST일 때만 작업명을 큐에 추가한다.
# - COMPLETE일 때 큐가 비어 있으면 False.
# - COMPLETE 대상이 queue[0]과 같아야 한다.
# - 일치하면 pop(0)으로 가장 앞의 작업을 제거한다.
# - 모든 로그를 처리한 뒤 큐가 비어 있어야 True.


def validate_processing(logs):
    result = []

    for log in logs:
        action, task = log.split()

        if action == "REQUEST":
            result.append(task)

        else:
            if len(result) == 0:
                return False

            if result[0] == task:
                result.pop(0)
            else:
                return False

    if len(result) == 0:
        return True
    else:
        return False


print(validate_processing(logs))


# 시간복잡도
# list.pop(0)은 뒤 원소를 당겨야 하므로 O(N).
# 전체적으로 최악의 경우 O(N^2)가 될 수 있다.
#
# 실전에서는 collections.deque를 사용하면
# append() / popleft()가 O(1)이므로 Queue 구현에 더 적합하다.
#
# 기억할 패턴
# Stack = LIFO -> 마지막 원소 확인 / pop()
# Queue = FIFO -> 첫 번째 원소 확인 / popleft()
