# Sentence Embedding

문장 전체를 벡터로 표현하고 문장 간 의미 유사도를 계산하는 방법을 비교한 실습입니다.

## 학습 내용

- BERT의 `last_hidden_state`에서 CLS Token Embedding 추출
- CLS Embedding 간 Cosine Similarity 계산
- `SentenceTransformer(all-MiniLM-L6-v2)`로 문장 임베딩 생성
- SentenceTransformer의 `util.cos_sim`을 이용한 문장 유사도 비교

## 파일

- `CLS.py` : BERT CLS Token 기반 문장 표현 실습
- `sentence.py` : SentenceTransformer 기반 문장 임베딩과 유사도 계산

이후 RAG Retrieval에서 질문과 Chunk의 의미 유사도를 비교하는 기반 개념으로 연결했습니다.
