# 2026-11-09 Python - DFS 기초 (Stack)
# 문제: 1번 노드부터 DFS로 탐색해 아래 방문 순서를 반환한다.
# 기대 결과: [1, 2, 4, 5, 3, 6]
#
# 이웃 목록에서 왼쪽 노드부터 방문하기 위해
# Stack에 넣을 때는 reversed(graph[current])를 사용한다.

graph = {
    1: [2, 3],
    2: [1, 4, 5],
    3: [1, 6],
    4: [2],
    5: [2],
    6: [3]
}

start = 1


# 직접 완성한 풀이
def dfs(graph, start):
    stack = [start]
    visited = []

    while stack:
        current = stack.pop()

        if current not in visited:
            visited.append(current)

            for node in reversed(graph[current]):
                if node not in visited:
                    stack.append(node)
    return visited


print(dfs(graph, start))  # [1, 2, 4, 5, 3, 6]


# 학습 중 막혔던 부분
# 1. DFS를 어디서부터 시작해야 할지 몰랐다.
#    -> BFS와 골격은 비슷하지만 Stack의 pop()으로 마지막 원소부터 꺼낸다.
# 2. for문을 왜 if current not in visited 안에 두는지 질문했다.
#    -> 이미 처리한 노드의 이웃을 다시 확장하지 않기 위해서다.
# 3. Stack에 [2, 3]을 그 순서로 추가하면 3이 먼저 꺼내진다.
#    -> 2를 먼저 방문하려면 [3, 2] 순서로 push해야 한다.
#
# 개선 포인트
# 방문 여부 검색을 set으로 바꾸면 membership 확인이 평균 O(1)이다.
# 단, 방문 순서를 유지할 별도의 리스트는 필요하다.
# 이 예제에서는 직접 작성한 코드가 요구한 결과를 만든다.
#
# 시간복잡도
# set으로 방문 여부를 관리하는 일반적인 인접 리스트 DFS: O(V + E).
# 현재 리스트 visited 방식은 membership 검색 때문에 더 느려질 수 있다.
#
# 기억할 패턴
# DFS = Stack(LIFO) + 방문 처리 + 이웃 확장
# visited에 이미 있는 노드는 다시 확장하지 않는다.
