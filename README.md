# Study Project

AI/NLP부터 RAG, Backend, Database, Docker, CI/CD까지 학습하며 **개념을 직접 코드로 구현하고 기록한 저장소**입니다.

단순히 라이브러리 사용법을 따라가는 것보다, 기술이 왜 필요한지 이해하고 작은 실습으로 확인한 뒤 서로 연결되는 흐름을 익히는 것을 목표로 했습니다.

[![CI](https://github.com/bigdata142857-create/Study_project/actions/workflows/ci.yml/badge.svg)](https://github.com/bigdata142857-create/Study_project/actions/workflows/ci.yml)

## 학습 흐름

`Statistical NLP → RNN/LSTM/Attention → Embedding → GPT Decoder → Sentence Embedding → Chunking → RAG → RAG Evaluation → Backend/DB → Docker → CI/CD`

## 주요 학습 영역

| 영역 | 학습/구현 내용 | 디렉토리 |
|---|---|---|
| Statistical NLP | N-gram, 빈도 기반 다음 단어 예측 | [01.statistical_NLP](./01.statistical_NLP/) |
| Sequence Model | RNN, LSTM Gate, Attention | [02. RNN, LSTM, Attention](./02.%20RNN%2C%20LSTM%2C%20Attention/) |
| Data Modeling | dict, dataclass, Pydantic 기반 데이터 검증 | [02.data_modeling_vertification](./02.data_modeling_vertification/) |
| Embedding | Token ID와 `nn.Embedding` | [03. Embedding & Positional](./03.%20Embedding%20%26%20Positional/) |
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

## 사용 기술

**Language**  
Python, SQL

**AI / Data**  
PyTorch, Transformers, Sentence Transformers, Scikit-learn, Pandas, NumPy

**Backend / Database**  
FastAPI, Pydantic, PostgreSQL, SQLAlchemy

**Infra / Tools**  
Docker, Docker Compose, Git, GitHub, GitHub Actions, Linux

## 학습 방식

1. 개념을 이해하고 핵심 동작을 작은 코드로 직접 구현합니다.
2. 실행 결과를 확인하며 입력·출력 형태와 내부 흐름을 이해합니다.
3. 여러 기술이 연결되는 단계에서는 파이프라인 단위로 실습합니다.
4. 실패한 테스트나 오류도 원인을 확인하고 수정 과정을 기록합니다.

각 디렉토리의 `README.md`에 해당 실습의 목적과 구현 내용을 정리했습니다.
