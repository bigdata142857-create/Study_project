# 2026-11-13 Python - BFS로 연결된 서버 그룹 개수 구하기
# 풀이 완료: 2026-11-15
#
# 문제
# 직접 또는 간접적으로 연결된 서버를 같은 그룹으로 간주한다.
# 전체 서버 그룹의 개수를 반환한다.
# 독립된 서버도 하나의 그룹이다.
# 빈 그래프는 0을 반환한다.
#
# 기대 결과: 4
# 그룹: [1,2,3], [4,5], [6], [7]

import collections

graph = {
    1: [2, 3],
    2: [1, 3],
    3: [1, 2],
    4: [5],
    5: [4],
    6: [],
    7: []
}


# 1. 첫 시도: 시작점 하나에서만 BFS를 하려고 함
# (풀이 중 사용한 핵심 코드 기록)
#
# def count_server_groups(graph):
#     start = list(graph)[0]
#     deq = collections.deque([start])
#     visited = []
#     while deq:
#         current = deq.popleft()
#         if current not in visited:
#             visited.append(current)
#
# 문제점: 서로 떨어진 그룹이 있으므로 첫 시작점에서만 탐색하면 전부 세지 못함.
# 해결 방향: 전체 노드를 돌면서 미방문 서버가 발견될 때마다 BFS를 새로 시작한다.


# 2. 중간 시도: 연결된 이웃을 visited에만 넣음
#
# for node in graph[current]:
#     if node not in visited:
#         visited.append(node)
#
# 문제점: 방문한 이웃을 Queue에 추가하지 않으면 그 이웃의 이웃을 확인할 수 없음.
# 예: 1 - 2 - 3에서는 1에서 2만 기록하고 3까지 확장하지 못함.


# 3. 최종 풀이: 직접 수정하여 완성
def count_server_groups(graph):
    visited = []
    count = 0

    for start in graph:
        if start not in visited:
            count += 1

            deq = collections.deque([start])
            visited.append(start)

            while deq:
                current = deq.popleft()

                for node in graph[current]:
                    if node not in visited:
                        visited.append(node)
                        deq.append(node)

    return count


print(count_server_groups(graph))  # 4

# 추가 반례: 직접 연결된 이웃을 Queue에 다시 넣지 않으면 오답이 발생한다.
graph2 = {
    1: [2],
    2: [1, 3],
    3: [2]
}
print(count_server_groups(graph2))  # 1
print(count_server_groups({}))      # 0


# 4. 개선 방향
# 리스트 visited에서 'in' 연산은 O(V)일 수 있다.
# 대형 그래프에서는 set으로 바꾸면 방문 여부를 평균 O(1)에 검사할 수 있다.
def count_server_groups_with_set(graph):
    visited = set()
    count = 0

    for start in graph:
        if start in visited:
            continue

        count += 1
        visited.add(start)
        queue = collections.deque([start])

        while queue:
            current = queue.popleft()

            for next_node in graph[current]:
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append(next_node)

    return count


print(count_server_groups_with_set(graph))  # 4

# 시간복잡도
# set 사용 + 인접 리스트: O(V + E), V=서버 수, E=연결 수
# 원본처럼 리스트로 visited를 관리하면 membership 검사가 O(V)이므로 더 느려질 수 있음.
#
# 다음에 기억할 패턴
# for 모든 노드:
#     미방문이면 그룹 개수 +1
#     Queue에 시작점 추가 + 방문 처리
#     BFS로 연결된 전체 노드를 방문 처리
#
# 주의: 방문 기록은 그룹 사이에서도 공유하고, Queue는 그룹마다 새로 생성한다.
