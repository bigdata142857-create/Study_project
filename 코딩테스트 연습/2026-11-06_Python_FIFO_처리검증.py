# 2026-11-06 Python - FIFO 처리 검증
# 핵심: Queue / FIFO

logs = [
    "REQUEST A",
    "REQUEST B",
    "COMPLETE A",
    "REQUEST C",
    "COMPLETE B",
    "COMPLETE C",
]

def validate_processing(logs):
    result = []

    for log in logs:
        value, key = log.split()

        if value == "REQUEST":
            result.append(key)
        else:
            if len(result) == 0:
                return False

            if result[0] == key:
                result.pop(0)
            else:
                return False

    return len(result) == 0

print(validate_processing(logs))

# 첫 시도에서의 핵심 실수
# - COMPLETE도 큐에 추가하려고 생각함
# - FIFO에서는 가장 먼저 들어온 항목(result[0])과 COMPLETE 대상을 비교해야 함
# - list.pop(0)은 O(N)이므로 실전에서는 collections.deque + popleft()가 더 적절함

# 기억할 패턴
# Queue = FIFO
# REQUEST -> 뒤에 추가
# COMPLETE -> 맨 앞 확인 후 제거
