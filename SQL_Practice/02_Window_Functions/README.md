# SQL Day 2 — Window Functions

PostgreSQL에서 주문 상태 변경 이력과 고객별 주문 금액을 이용해 Window Function을 학습했습니다.

- 학습일: 2026-10-17
- 사용 기술: PostgreSQL, SQL
- 주제: ROW_NUMBER(), RANK(), DENSE_RANK(), LAG(), PARTITION BY, CTE, INTERVAL, EXTRACT(EPOCH)
- 데이터: 직접 구성한 가상 주문 데이터(실제 기업 데이터 아님)

## 파일 구성

| 파일 | 내용 |
| --- | --- |
| 01_create_tables.sql | 스키마, 테이블 2개 생성 및 샘플 데이터 입력 |
| 02_window_ranking.sql | Q1 최신 상태 조회, Q2 고객별 주문 금액 순위 |
| 03_event_timing.sql | Q3 이전 주문 상태 조회, Q4 이벤트 간 소요 시간 |

## 테이블

- de_practice.order_events: 상태 변경 이력 12행. event_id, order_id, status, changed_at.
- de_practice.customer_orders: 주문 금액 정보 10행. order_id, customer_id, amount, ordered_at.

두 테이블은 각기 다른 독립 실습 데이터입니다. order_id가 두 테이블에서 서로 다른 범위로 구성되어 있으며 JOIN하지 않습니다.

## 실행 방법

PostgreSQL 접속 후 아래 순서대로 실행합니다.

~~~bash
psql -d YOUR_DATABASE -f "SQL_Practice/02_Window_Functions/01_create_tables.sql"
psql -d YOUR_DATABASE -f "SQL_Practice/02_Window_Functions/02_window_ranking.sql"
psql -d YOUR_DATABASE -f "SQL_Practice/02_Window_Functions/03_event_timing.sql"
~~~

스키마 및 테이블을 삭제하지 않습니다. INSERT는 기본키 충돌 시 삽입을 건너뛰므로 반복 실행할 수 있지만, 이미 들어 있는 행을 초기 상태로 되돌리지는 않습니다. 정확한 예제 결과를 위해 비어 있는 실습 DB를 권장합니다.

## Q1. 주문별 최신 상태 — ROW_NUMBER

고객의 주문 상태 변경 기록이 여러 번 남아 있어도, order_id별 최신 기록 1개만 조회합니다.

- PARTITION BY order_id: 주문번호별 순번을 따로 계산
- ORDER BY changed_at DESC, event_id DESC: 최신 시간 우선, 시간이 같으면 더 큰 event_id 우선
- CTE 내부에서 rn을 만든 후 바깥 WHERE rn = 1로 필터링
- 예상 결과: 5행. 주문 201=DELIVERED, 202=SHIPPED, 203=CANCELED, 204=PAID, 205=CREATED.

## Q2. 고객별 주문 금액 순위 — RANK와 DENSE_RANK

같은 고객의 주문에 같은 금액이 존재할 때 동일한 순위를 부여합니다.

- PARTITION BY customer_id, ORDER BY amount DESC
- RANK: 공동 1위가 두 건이면 다음 순위는 3위
- DENSE_RANK: 공동 1위가 두 건이면 다음 순위는 2위
- 최종 출력 정렬의 order_id ASC는 동점 순위를 바꾸지 않음
- 예상 결과: 10행. 고객 101의 금액 120000, 120000, 70000, 40000에 대한 순위는 RANK 1/1/3/4, DENSE_RANK 1/1/2/3.

## Q3. 이전 주문 상태 — LAG

현재 이벤트의 바로 이전 상태를 조회합니다.

- LAG(status)는 앞선 행의 status 값을 가져옴
- PARTITION BY order_id: 서로 다른 주문의 상태가 섞이지 않도록 분리
- ORDER BY changed_at ASC, event_id ASC: 상태 변경 순서를 과거부터 결정
- 첫 번째 이벤트에는 이전 행이 없어 prev_status가 NULL
- 예상 결과: 12행. 주문 201: CREATED(NULL) → PAID(CREATED) → SHIPPED(PAID) → DELIVERED(SHIPPED).

## Q4. 상태 변경 소요 시간 — LAG와 EXTRACT

현재 이벤트 시간에서 이전 이벤트 시간을 뺀 뒤 분 단위로 계산합니다.

1. LAG(changed_at)으로 이전 시각을 조회
2. changed_at - 이전 시각 = INTERVAL
3. EXTRACT(EPOCH FROM INTERVAL) = 초 단위 숫자
4. 초 / 60 = 분 단위 숫자

Q4는 학습 중 prev_changed_at과 시간 차이까지 직접 작성한 뒤, EXTRACT()로 식을 감싸는 방법을 설명받아 완성했습니다. 기존 prev_changed_at 컬럼도 중간 계산 검증용으로 출력합니다.

- 예상 결과: 12행, 최초 이벤트의 elapsed_minutes는 NULL
- 주문 201: CREATED→PAID 10분, PAID→SHIPPED 110분, SHIPPED→DELIVERED 1680분.

### 이해도를 확인하며 수정한 점

- ROW_NUMBER()에는 빈 괄호가 필요하고, AS rn은 OVER(...) 바깥에 둡니다.
- GROUP BY는 집계로 행을 묶지만, PARTITION BY는 원본 행을 유지하며 순위를 계산합니다.
- DENSE_RANK()는 밑줄이 있는 함수 이름입니다.
- LAG(status)와 LAG(changed_at)은 이전 행에서 가져올 컬럼이 서로 다릅니다.
- '2 hours 30 minutes'는 2.5시간이지만, EXTRACT(EPOCH ...)/60 결과는 150분입니다.

## 검증 상태

문법과 논리는 대화에서 검토하여 정리한 예제입니다. GitHub에 업로드하기 전에 별도 PostgreSQL 서버에서 모든 스크립트의 실제 실행 결과를 직접 확인하지는 않았습니다. 위 결과는 삽입할 샘플 데이터에 따른 예상 값입니다.

다음 단계로는 실제 PostgreSQL에서 각 쿼리를 실행하고 행 수·NULL·동점 순위를 확인할 계획입니다.
