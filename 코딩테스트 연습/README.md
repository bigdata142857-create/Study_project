# 코딩테스트 연습

데이터 엔지니어 코딩테스트 대비 기록입니다.

정답만 저장하지 않고 다음 순서로 기록합니다.

1. 문제
2. 처음 시도
3. 왜 틀렸거나 아쉬웠는지
4. 수정한 풀이
5. 시간복잡도
6. 다음에 기억할 패턴

## 진행 현황

| 날짜 | 주제 | 문제 | 핵심 |
|---|---|---|---|
| 2026-10-21 | SQL / Window Function | 고객별 최신 주문 찾기 | PARTITION BY 기준 |
| 2026-10-25 | Python / dict | 사용자별 최신 이벤트 | key 설계와 전체 레코드 교체 |
| 2026-10-26 | Hash / 빈도 계산 | 가장 많이 발생한 에러 코드 | 값 → 빈도수 |
| 2026-10-26 | Hash / 탐색 | 목표 금액을 만드는 두 거래 | 값 → 인덱스 |
| 2026-10-27 | SQL / 집계 | 실패가 많은 파이프라인 찾기 | JOIN, CASE WHEN, HAVING |
| 2026-10-27 | Python / 중첩 dict | 서버별 OK/FAIL 집계 | result[group][status] += 1 |
| 2026-10-28 | Python / 상태 누적 | 서버별 실패 횟수와 마지막 상태 | 초기화와 공통 갱신 분리 |
| 2026-10-28 | SQL / Window Function | 고객별 이전 주문 금액 | LAG, PARTITION BY, ORDER BY |
| 2026-10-29 | Python / 연속 구간 | 누락 배치 구간 찾기 | start / prev / current |
| 2026-10-29 | SQL / LEFT JOIN | 실행 이력 없는 파이프라인 포함 집계 | LEFT JOIN, SUM(CASE) |
| 2026-10-31 | Python / Stack | START/END 로그 검증 | LIFO, top 확인, pop |
| 2026-10-31 | SQL / Window Function | 파이프라인별 최근 실행 1건 | ROW_NUMBER + CTE |
| 2026-11-04 | Python / 집계·정렬 | 장애 서버 TOP 3 | 다중 정렬 key |
| 2026-11-04 | SQL / 최근 N건 집계 | 최근 3회 중 FAIL 2회 이상 | ROW_NUMBER → WHERE → GROUP BY → HAVING |

## 현재 자주 하는 실수

- 문제에서 "무엇마다 하나를 뽑는지"와 PARTITION BY 기준을 다르게 잡는 실수
- Window Function에서 PARTITION BY를 빼서 그룹 경계가 섞이는 실수
- Window Function과 GROUP BY 집계를 같은 단계에서 처리하려는 실수
- 집계가 필요하지 않은 문제에도 GROUP BY를 습관적으로 넣는 실수
- CASE WHEN에서 THEN / ELSE / END 문법을 빠뜨리는 실수
- COUNT(CASE WHEN ... THEN 1 ELSE 0 END)처럼 0도 COUNT된다는 점을 놓치는 실수
- 집계 결과 조건을 WHERE에 두고 HAVING을 놓치는 실수
- CTE 바깥에서 쓸 컬럼을 CTE SELECT에 포함하지 않는 실수
- Window Function 결과를 같은 SELECT의 WHERE에서 바로 필터링하려는 실수
- 최신 1건 문제에서 DENSE_RANK와 ROW_NUMBER의 차이를 놓치는 경우
- 딕셔너리의 일부 필드만 갱신해서 서로 다른 시점의 데이터가 섞이는 실수
- sorted()가 원본을 바꾸는 함수라고 착각하는 실수
- dict를 쓸 때 key와 value 방향을 문제 목적에 맞게 잡지 못하는 경우
- dict 안의 dict에서 현재 상태값 자체를 key로 쓸 수 있는데도 별도 조건문을 만들려는 경우
- 처음 등장할 때만 필요한 처리와 매 행마다 필요한 처리를 분리하지 못해 코드가 중복되는 경우
- 연속 구간 문제에서 start / prev / current 역할을 섞는 경우
- 마지막 구간은 반복문 안에서 확정되지 않을 수 있다는 점을 놓치는 경우
- Stack 문제에서 "존재 여부"만 보고 마지막 원소인지 확인하지 않는 경우
- remove()와 pop()의 역할/복잡도 차이를 놓치는 경우
- 서로 다른 형태의 값을 membership으로 비교해 불필요한 조건을 만드는 경우
- 정답을 찾은 뒤에도 불필요하게 반복하는 경우

## 연습 원칙

- 먼저 직접 풀이한다.
- 틀린 코드는 삭제하지 않고 기록한다.
- 왜 틀렸는지를 한 문장으로 설명할 수 있을 때까지 복습한다.
- 최종 코드뿐 아니라 시간복잡도까지 확인한다.
- 다음날 비슷한 문제를 다른 상황으로 다시 풀어본다.
- 막혔을 때는 바로 정답을 보지 않고 단계별 힌트를 받는다.
- 힌트 1: 잘못된 위치나 생각 방향만 확인한다.
- 힌트 2: 사용할 자료구조/함수의 성격만 확인한다.
- 힌트 3: 코드 골격까지만 확인한다.
- 최종 정답은 직접 수정 시도 후 확인한다.

## 현재 학습 방향

데이터 엔지니어 / DBA / 데이터 직무 전형을 고려해 다음 세 축을 함께 연습한다.

- SQL: JOIN, GROUP BY, HAVING, CASE, CTE, Subquery, Window Function
- Python 코테: dict/set, 정렬, 문자열, Stack/Queue, 완전탐색, BFS/DFS 기초
- 실무형 데이터 처리: 로그 집계, 중복 제거, 최신값 선택, 상태 관리, CSV/JSON 처리

목표는 어려운 문제를 빨리 푸는 것보다, 자주 나오는 기본 패턴을 힌트 없이 15~20분 안에 구현할 수 있도록 만드는 것이다.
