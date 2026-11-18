# 2026-11-16 Python 코딩테스트 — 서버 간 최단 연결 거리 (BFS)
#
# [문제]
# 서버 연결은 양방향이고 모든 간선의 이동 비용이 동일하다.
# start에서 target까지의 최소 연결 횟수를 반환한다.
# 연결할 수 없으면 -1, start == target이면 0을 반환한다.
# start와 target은 graph에 존재한다고 가정한다.
#
# [학습 기록] 최초 시도 → 오류 수정 → 최종 풀이


import collections

graph = {
    1: [2, 3],
    2: [1, 4],
    3: [1, 5],
    4: [2, 6],
    5: [3, 6],
    6: [4, 5],
    7: []
}


# 1. 첫 시도: Queue를 만들었지만 start의 이웃만 확인하려 함
#
# def shortest_server_hops(graph, start, target):
#     dequ = collections.deque([start])
#     distance = {start: 0}
#     while dequ:
#         for node in graph[start]:
#             ...
#
# 문제점:
# - graph[start]를 반복하면 탐색 시작점의 이웃만 본다.
# - BFS에서는 current = dequ.popleft()로 현재 노드를 꺼낸 뒤
#   graph[current]의 이웃을 확인해야 한다.


# 2. 중간 시도: distance에 잘못된 자료형을 저장하고 매번 증가시킴
#
# while dequ:
#     current = dequ.popleft()
#     for node in graph[current]:
#         if node not in distance:
#             distance[node] = {1}
#         distance[node] += 1
#
# 문제점:
# - {1}은 정수 1이 아니라 set 자료형이다.
# - 이미 방문한 서버에서도 거리를 계속 증가시키면 최단 거리가 깨진다.
# - 새로 발견한 서버의 거리는 distance[current] + 1이다.
# - 새로 발견한 서버를 Queue에도 넣어야 추가로 탐색할 수 있다.


# 3. 다음 시도: BFS는 정확했지만 반환 부분에서 예외가 발생할 수 있었음
#
# return distance[target]
#
# target이 도달 불가능한 서버라면 distance에 키가 없으므로 KeyError 발생.
# -> distance.get(target, -1)로 수정.


# 4. 최종 정답 — 직접 작성한 코드
def shortest_server_hops(graph, start, target):
    dequ = collections.deque([start])
    distance = {start: 0}

    while dequ:
        current = dequ.popleft()

        for node in graph[current]:
            if node not in distance:
                distance[node] = distance[current] + 1
                dequ.append(node)

    return distance.get(target, -1)


# 5. 확인할 테스트
assert shortest_server_hops(graph, 1, 6) == 3
assert shortest_server_hops(graph, 1, 4) == 2
assert shortest_server_hops(graph, 1, 7) == -1
assert shortest_server_hops(graph, 3, 3) == 0
assert shortest_server_hops(graph, 3, 2) == 2

print(shortest_server_hops(graph, 1, 6))  # 3


# 6. 탐색 흐름 (start = 1)
# distance = {1: 0}
# current = 1 -> 2, 3 발견 -> distance[2] = 1, distance[3] = 1
# current = 2 -> 4 발견    -> distance[4] = 2
# current = 3 -> 5 발견    -> distance[5] = 2
# current = 4 -> 6 발견    -> distance[6] = 3
#
# distance 딕셔너리는 '방문 여부'와 '시작점에서의 최단 거리'를 함께 관리한다.
# BFS는 간선 비용이 모두 동일할 때 가까운 정점부터 탐색하므로
# 처음 방문한 순간 기록한 거리가 최단 거리다.
#
# 시간복잡도: O(V + E) — V는 서버 수, E는 간선 수
# 공간복잡도: O(V) — distance와 Queue
#
# 다음에 기억할 패턴:
#   Queue 생성 + 시작점 거리 0
#   while Queue:
#       current = popleft()
#       미방문 이웃:
#           distance[이웃] = distance[current] + 1
#           append(이웃)
#   return distance.get(target, -1)
