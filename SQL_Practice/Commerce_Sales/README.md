# Commerce Sales SQL Practice

데이터 엔지니어 과제 전형을 대비해 PostgreSQL에서 가상의 커머스 주문·결제·환불 데이터를 조회하고, 중복 집계를 방지하면서 매출을 집계하는 SQL 실습입니다.

- 학습일: 2026-10-14
- 사용 기술: PostgreSQL, SQL
- 학습 주제: INNER JOIN, LEFT JOIN, GROUP BY, CTE(WITH), SUM, COUNT, COALESCE
- 데이터: 실습용으로 직접 정의한 가상 데이터. 실제 기업 데이터가 아닙니다.

## 파일 구성

| 파일 | 내용 |
| --- | --- |
| 01_create_tables.sql | 스키마·테이블 3개 생성 및 샘플 데이터 삽입 |
| 02_basic_queries.sql | Q1 정상 결제 주문 조회, Q2 날짜별 결제액 집계 |
| 03_revenue_analysis.sql | Q3 날짜별 순매출, Q4 서비스별·날짜별 순매출 |

## 테이블 구조

- orders: 주문 정보 (order_id PK, service_name, customer_id, ordered_at). 8건.
- payments: 결제 정보 (order_id PK/FK, amount, status). 8건, PAID 7건 및 FAILED 1건.
- refunds: 환불 정보 (refund_id PK, order_id FK, refund_amount). 4건.
- 연결: orders.order_id = payments.order_id = refunds.order_id.
- 현재 샘플에서는 주문 1건에 결제 정보는 최대 1건, 환불 정보는 여러 건이 존재할 수 있습니다.

## 실행 방법

PostgreSQL 데이터베이스에 접속한 뒤 아래 순서로 파일을 실행합니다. DBeaver 또는 pgAdmin에서도 같은 순서로 열어 실행할 수 있습니다.

~~~bash
psql -d YOUR_DATABASE -f "SQL_Practice/Commerce_Sales/01_create_tables.sql"
psql -d YOUR_DATABASE -f "SQL_Practice/Commerce_Sales/02_basic_queries.sql"
psql -d YOUR_DATABASE -f "SQL_Practice/Commerce_Sales/03_revenue_analysis.sql"
~~~

모든 테이블과 데이터는 de_practice 스키마에 생성됩니다. 초기 적재는 ON CONFLICT DO NOTHING으로 기존 기본키 행에 대한 중복 삽입을 피하지만, 기존 데이터의 내용까지 초기화하지는 않습니다. 가능하면 빈 실습 DB에서 실행하세요.

## 문제별 학습 내용

### Q1. 정상 결제 주문 조회

- orders와 payments를 order_id로 JOIN.
- status가 PAID인 주문만 조회.
- 주문번호 오름차순 정렬.
- 기대 결과: 7행.

### Q2. 날짜별 결제 총액

- 정상 결제 데이터만 날짜별 GROUP BY.
- COUNT(*)로 결제 건수, SUM(amount)로 결제 총액 계산.
- 예상 결과:

| ordered_at | payment_count | total_amount |
| --- | ---: | ---: |
| 2026-10-13 | 3 | 120000 |
| 2026-10-14 | 4 | 185000 |

### Q3. 날짜별 환불 반영 순매출

한 주문에 여러 환불 내역이 있을 때 refunds 원본을 곧바로 JOIN하면 결제 금액이 반복될 수 있습니다.

예: order_id 102는 결제 50,000원 1건과 환불 20,000원 / 5,000원 2건이 존재합니다. 원본 환불 2건을 직접 JOIN한 뒤 결제 금액을 SUM하면 50,000원이 두 번 계산됩니다.

해결 방식:

1. CTE(refund_summary)에서 order_id별 환불 합계를 먼저 계산합니다.
2. 주문별 1행으로 집계된 환불 결과를 결제 정보에 LEFT JOIN합니다.
3. COALESCE로 환불이 없는 경우를 0원으로 처리합니다.
4. 순매출 = 결제 총액 - 환불 총액.

예상 결과:

| ordered_at | total_amount | total_refund | net_revenue |
| --- | ---: | ---: | ---: |
| 2026-10-13 | 120000 | 25000 | 95000 |
| 2026-10-14 | 185000 | 30000 | 155000 |

### Q4. 서비스별·날짜별 순매출

Q3의 중복 방지 구조를 유지하면서 service_name과 ordered_at을 함께 GROUP BY합니다.

예상 결과:

| service_name | ordered_at | payment_count | total_amount | total_refund | net_revenue |
| --- | --- | ---: | ---: | ---: | ---: |
| 10x10 | 2026-10-13 | 1 | 40000 | 0 | 40000 |
| idus | 2026-10-13 | 2 | 80000 | 25000 | 55000 |
| 10x10 | 2026-10-14 | 1 | 20000 | 20000 | 0 |
| idus | 2026-10-14 | 2 | 75000 | 0 | 75000 |
| tumblbug | 2026-10-14 | 1 | 90000 | 10000 | 80000 |

## 학습하며 확인한 점

- customer_id는 고객의 고유 식별자여도 여러 주문에서 반복될 수 있어, 결제와 주문을 연결하는 키로 적합하지 않습니다. 이 실습에서는 order_id를 사용합니다.
- JOIN 전후의 데이터 단위(grain)를 확인해야 집계 금액과 COUNT가 부풀려지지 않습니다.
- CTE의 첫 GROUP BY는 주문별 환불 집계, 최종 GROUP BY는 날짜별 또는 날짜·서비스별 집계입니다.
- LEFT JOIN 결과에 환불이 없는 경우 NULL이 생성될 수 있으므로, 빼기 전에 환불 총액을 COALESCE(..., 0)으로 변환합니다.
- 이 예시의 순매출은 '주문일' 기준이며, 실제 업무의 환불 발생일 기준 지표나 회계상 매출과는 다를 수 있습니다.

## 검증 상태

대화에서 작성·검토한 SQL과 샘플 데이터로 정리한 학습용 예제입니다. 저장소 업로드 시 별도 PostgreSQL 서버에서 직접 실행한 결과를 확인하지 않았으며, 위 표는 제공된 샘플 데이터에 근거한 예상 값입니다.

다음 학습은 Python으로 파일을 읽어 검증하고 PostgreSQL에 적재하는 ETL 파이프라인 실습입니다.
