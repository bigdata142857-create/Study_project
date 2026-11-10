# 2026-11-09 Python - BFS 기초
# 문제: 그래프 1번 노드에서 시작해 BFS 방문 순서를 반환한다.
# 기대 결과: [1, 2, 3, 4, 5, 6]
#
#     1
#   /   \
#  2     3
# / \     \
# 4  5     6
#
# 학습 과정
# 1. 처음에는 while len(graph) == 0을 사용하려고 했다.
#    -> graph를 줄이는 것이 아니라 Queue에 할 일이 남아 있는 동안 반복해야 한다.
# 2. graph[current]의 이웃 목록 자체에서 pop()을 시도했다.
#    -> 그래프를 수정하지 않고 각 이웃을 Queue에 추가한다.
# 3. BFS의 기본 구조: Queue에서 하나 꺼내기 -> 미방문이면 방문 처리 -> 이웃 추가.

import collections

graph = {
    1: [2, 3],
    2: [1, 4, 5],
    3: [1, 6],
    4: [2],
    5: [2],
    6: [3]
}

start = 1


# 직접 완성한 풀이 (대화에서 작성한 코드)
def bfs(graph, start):
    deq = collections.deque([start])
    visited = []

    while deq:
        current = deq.popleft()

        if current not in visited:
            visited.append(current)

        for node in graph[current]:
            if node not in visited:
                deq.append(node)

    return visited


print(bfs(graph, start))  # [1, 2, 3, 4, 5, 6]


# 개선 이유
# 위 코드는 이 예제에서 올바른 방문 순서를 반환한다.
# 다만 방문 처리를 꺼낼 때 수행하므로 같은 노드가 Queue에 중복 추가될 수 있다.
# 또한 visited가 리스트여서 'in' 확인 비용이 O(V)이다.
#
# 개선 예시: 큐에 넣을 때 방문 처리하고, set으로 방문 여부 확인
def bfs_optimized(graph, start):
    queue = collections.deque([start])
    seen = {start}
    order = []

    while queue:
        current = queue.popleft()
        order.append(current)

        for node in graph[current]:
            if node not in seen:
                seen.add(node)
                queue.append(node)

    return order


print(bfs_optimized(graph, start))  # [1, 2, 3, 4, 5, 6]

# 시간복잡도
# 개선 버전: O(V + E), V=노드 수, E=간선 수.
# 직접 작성한 visited 리스트 방식은 탐색 때 선형 검색이 발생하고
# 중복 Queue 항목을 다시 확장할 수 있어 훨씬 느려질 수 있다.
#
# 기억할 패턴
# BFS = Queue(FIFO) + 방문 처리 + 이웃 확장
# 그래프 자체를 제거하거나 수정하면서 탐색하지 않는다.
