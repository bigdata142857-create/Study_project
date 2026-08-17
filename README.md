# Study Project

## 프로젝트 소개

AI, NLP, RAG, LLM 및 백엔드·인프라 관련 기술을 학습하고 직접 구현한 내용을 정리한 스터디 저장소입니다.

개념을 이해하는 것에 그치지 않고,
**NLP 기초 → Embedding → Transformer → RAG → API → Database → Docker → CI/CD**로 학습 범위를 확장하며 각 기술이 실제 서비스에서 어떻게 연결되는지 이해하는 것을 목표로 진행했습니다.

---

## 학습 목표

* NLP와 문장 임베딩의 기본 원리 이해
* Attention, Transformer, BERT, GPT 구조 학습
* 다양한 Chunking 및 Retrieval 방식 구현
* RAG 파이프라인 구성 및 평가 방법 학습
* FastAPI를 활용한 REST API 구현
* PostgreSQL 및 SQLAlchemy를 활용한 데이터베이스 연동
* Docker와 Docker Compose를 활용한 서비스 환경 구성
* GitHub Actions 기반 CI 과정 학습

---

## 주요 학습 영역

### NLP & Embedding

* Text Preprocessing
* Sentence Embedding
* Cosine Similarity
* Sentence Transformers

### Deep Learning & LLM

* RNN / LSTM
* Attention
* Transformer
* BERT
* GPT Decoder

### RAG

* Chunking
* Embedding
* Retrieval
* Parent-Child Retrieval
* Hierarchical Retrieval
* Multi-hop Retrieval
* Query Rewrite
* Post-Retrieval Processing
* Grounding
* Citation
* RAG Evaluation

### Backend & Database

* FastAPI
* REST API
* Pydantic
* PostgreSQL
* SQLAlchemy ORM
* Table / Relationship 설계
* CRUD

### Docker & CI/CD

* Dockerfile
* Docker Container
* Docker Compose
* Container Log / Shell
* Health Check
* GitHub Actions
* Test 및 Code Quality Check

---

## 사용 기술

**Language**

* Python
* SQL

**AI / Data**

* PyTorch
* Pandas
* NumPy
* Scikit-learn
* Sentence Transformers

**Backend / Database**

* FastAPI
* PostgreSQL
* SQLAlchemy

**Infra / Tools**

* Docker
* Docker Compose
* Git
* GitHub
* GitHub Actions
* Linux

---

## 학습 방향

각 실습은 단순히 라이브러리 사용법을 익히는 것보다
**기술이 필요한 이유와 내부 동작을 이해하고 직접 구현해보는 것**에 중점을 두었습니다.

초기에는 NLP와 딥러닝 모델 구조를 중심으로 학습했으며, 이후 RAG를 구현하면서 검색과 생성 과정까지 범위를 확장했습니다.

이후에는 모델과 RAG 기능을 실제 서비스 형태로 구성하기 위해 FastAPI, Database, Docker, CI/CD 등을 학습하며 AI 기능이 애플리케이션과 시스템 환경에서 동작하는 전체 흐름을 이해하고자 했습니다.

---

## Repository

각 디렉토리에는 해당 주제에 대한 실습 코드와 학습 내용을 정리하고 있습니다.

```text
Study_project/
├── NLP
├── Embedding
├── Transformer
├── RAG
├── FastAPI
├── Database
├── Docker
├── RAG_Evaluation
├── CI_CD
└── ...
```

현재도 새로운 기술을 학습하고 실습한 내용을 지속적으로 추가하고 있습니다.
