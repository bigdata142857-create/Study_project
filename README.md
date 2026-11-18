# Study Project

Python, SQL, PostgreSQL, Docker 및 AI/NLP·RAG를 직접 실습하며 학습 내용을 정리한 저장소입니다.

초기에는 언어 모델의 구조와 RAG 파이프라인을 중심으로 학습했고, 이후에는 데이터베이스·데이터 처리·알고리즘과 시스템 기초까지 범위를 확장했습니다. 실행 결과뿐 아니라 처음 시도한 코드, 오류의 원인, 수정한 이유를 기록하는 것을 중요하게 생각합니다.

[![CI](https://github.com/bigdata142857-create/Study_project/actions/workflows/ci.yml/badge.svg)](https://github.com/bigdata142857-create/Study_project/actions/workflows/ci.yml)

## 현재 중점적으로 학습하는 내용

| 영역 | 학습 주제 | 기록 위치 |
|---|---|---|
| Python 코딩테스트 | dict/set, 정렬, Stack·Queue, BFS·DFS, 상태·로그 처리 | [코딩테스트 연습](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/) |
| SQL 코딩테스트 | JOIN, GROUP BY, HAVING, CTE, Window Function, 최신 데이터 추출 | [코딩테스트 연습](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/) |
| SQL 실습 | 분석 쿼리 및 Window Function 관련 문제 | [SQL_Practice](./SQL_Practice/) |
| PostgreSQL / DB | 테이블 구성, SQLAlchemy ORM, 데이터 조회 및 처리 | [06.DB_practice](./06.DB_practice/) |
| 인프라 기초 | FastAPI, Docker Compose, PostgreSQL 연동·상태 확인 | [07_docker_practice](./07_docker_practice/) |
| 개념 공부 | Linux 명령어, 접근 권한, 암호화·해시·키 관리 기초 | [개념 공부 기록](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/2026-11-08_%EA%B0%9C%EB%85%90%EA%B3%B5%EB%B6%80_%EC%95%94%ED%98%B8%ED%99%94_Linux.md) |

코딩테스트 풀이 기록은 단순 정답 모음이 아닙니다. 최초 접근 방식 → 틀린 이유 → 수정 과정 → 최종 풀이 → 다음에 기억할 패턴 순서로 정리합니다.

## 최근 학습 기록

| 날짜 | 주제 | 배운 점 |
|---|---|---|
| 2026-11-18 | [중복 메타데이터 탐지 SQL](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/2026-11-18_SQL_%EC%A4%91%EB%B3%B5%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0_%EC%A0%95%EB%A6%AC%EB%8C%80%EC%83%81%ED%83%90%EC%A7%80.sql) | 복합 PARTITION BY, 최신 행 유지와 과거 중복 기록 조회 구분 |
| 2026-11-16 | [서버 간 최단 연결 거리 BFS](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/2026-11-16_Python_%EC%84%9C%EB%B2%84%EA%B0%84_%EC%B5%9C%EB%8B%A8%EC%97%B0%EA%B2%B0%EA%B1%B0%EB%A6%AC_BFS.py) | Queue 탐색, distance로 최단 거리·방문 여부 관리, 미도달 -1 처리 |
| 2026-11-15 | [사용자별 최근 로그인 상태 SQL](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/2026-11-15_SQL_%EC%82%AC%EC%9A%A9%EC%9E%90%EB%B3%84_%EC%B5%9C%EA%B7%BC%EB%A1%9C%EA%B7%B8%EC%9D%B8%EC%83%81%ED%83%9C.sql) | ROW_NUMBER로 최신 1건 선정, LEFT JOIN으로 기록 없는 사용자 유지, COALESCE로 NULL 처리 |
| 2026-11-13 ~ 11-15 | [서버 연결 그룹 개수 BFS](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/2026-11-13_Python_%EC%84%9C%EB%B2%84%EC%97%B0%EA%B2%B0%EA%B7%B8%EB%A3%B9_BFS.py) | 미방문 서버를 기준으로 BFS 반복, Queue에 이웃 추가, 방문 집합 공유 |
| 2026-11-10 | [DB 사용자별 접속 기록 집계](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/2026-11-10_SQL_%EC%82%AC%EC%9A%A9%EC%9E%90%EB%B3%84_%EC%A0%91%EC%86%8D%EA%B8%B0%EB%A1%9D_%EC%A7%91%EA%B3%84.sql) | LEFT JOIN, COUNT, SUM(CASE), MAX |
| 2026-11-09 | [BFS 기초](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/2026-11-09_Python_BFS_%EA%B8%B0%EC%B4%88.py) / [DFS 기초](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/2026-11-09_Python_DFS_%EA%B8%B0%EC%B4%88.py) | Queue·Stack과 방문 순서의 차이 |
| 2026-11-08 | [Linux·암호화 개념](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/2026-11-08_%EA%B0%9C%EB%85%90%EA%B3%B5%EB%B6%80_%EC%95%94%ED%98%B8%ED%99%94_Linux.md) | 로그·포트·프로세스 확인, 해시와 대칭키·비대칭키 구분 |

전체 진행 현황과 풀이별 기록은 [코딩테스트 연습 README](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/README.md)에서 확인할 수 있습니다.

## 기존 AI / Data 학습 경로

`Statistical NLP → RNN/LSTM/Attention → Embedding → GPT Decoder → Sentence Embedding → Chunking → RAG → RAG Evaluation → Backend/DB → Docker → CI/CD`

초기에 실습했던 AI/NLP·RAG 및 Backend 관련 코드는 기존 디렉터리에 유지하고 있습니다.

## 디렉터리 안내

| 분류 | 내용 | 디렉터리 |
|---|---|---|
| NLP 기초 | N-gram, 빈도 기반 다음 단어 예측 | [01.statistical_NLP](./01.statistical_NLP/) |
| Sequence Model | RNN, LSTM Gate, Attention | [02. RNN, LSTM, Attention](./02.%20RNN%2C%20LSTM%2C%20Attention/) |
| Data Modeling | dict, dataclass, Pydantic 기반 데이터 검증 | [02.data_modeling_vertification](./02.data_modeling_vertification/) |
| Embedding | Token ID와 nn.Embedding | [03. Embedding & Positional](./03.%20Embedding%20%26%20Positional/) |
| LLM Structure | GPT Decoder block 구조 | [04.GPT_decoder](./04.GPT_decoder/) |
| Sentence Embedding | BERT CLS, SentenceTransformer, Cosine Similarity | [05.Sentence_embedding](./05.Sentence_embedding/) |
| Chunking | Overlap, Recursive, Semantic Chunking | [06.Chunking](./06.Chunking/) |
| Database | PostgreSQL, SQLAlchemy ORM | [06.DB_practice](./06.DB_practice/) |
| RAG Basics | Relevance/Correctness 유사도 실습 | [07.RAG_cor](./07.RAG_cor/) |
| Docker Practice | FastAPI + PostgreSQL + Docker Compose + Health Check | [07_docker_practice](./07_docker_practice/) |
| RAG Retrieval | Parent-Child Retrieval, Multi-hop Retrieval, 평가 데이터셋 | [08. RAG_평가](./08.%20RAG_%ED%8F%89%EA%B0%80/) |
| RAG Reliability | Post-retrieval Filtering/Deduplication/Clustering | [09.Post-retrieval·Multi-turn RAG·Reliability](./09.Post-retrieval%C2%B7Multi-turn%20RAG%C2%B7Reliability/) |
| CI/CD | FastAPI 테스트, Black/Ruff/Mypy/Pytest, GitHub Actions | [10.CI_CD](./10.CI_CD/) |
| 공동 실습 | TF-IDF, Attention, FastAPI, RAG pipeline, Git 협업 실습 | [joint_practice](./joint_practice/) |
| SQL Practice | Window Function, 데이터 조회·분석 실습 | [SQL_Practice](./SQL_Practice/) |
| 코딩테스트 연습 | Python 알고리즘, SQL 문제 풀이와 오답 기록, 개념 공부 | [코딩테스트 연습](./%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%97%B0%EC%8A%B5/) |

## 사용 기술 및 학습 도구

- Language: Python, SQL
- AI / Data: PyTorch, Transformers, Sentence Transformers, Scikit-learn, Pandas, NumPy
- Backend / Database: FastAPI, Pydantic, PostgreSQL, SQLAlchemy
- Infra / Tools: Docker, Docker Compose, Git, GitHub, GitHub Actions, Linux 명령어 기초

위 기술들은 저장소 전반에서 실습하거나 학습한 항목이며, 모든 기술에 대해 동일한 수준의 숙련도를 의미하지는 않습니다.

## 학습 기록 원칙

1. 개념을 먼저 이해하고 직접 코드를 작성합니다.
2. 오답과 시행착오를 지우지 않고, 왜 수정했는지 남깁니다.
3. 테스트 예제뿐 아니라 경계 조건·반례도 확인합니다.
4. SQL은 집계와 행 선택의 차이, JOIN과 NULL 처리 등을 구분해 기록합니다.
5. Python은 자료구조 선택 이유와 시간복잡도를 함께 살펴봅니다.

학습 내용은 진행에 따라 추가·수정합니다.
