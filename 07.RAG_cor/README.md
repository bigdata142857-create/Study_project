# RAG Evaluation Basics

질문·답변 텍스트를 벡터화하고 Cosine Similarity로 비교하면서 RAG 평가의 기초 개념을 확인한 실습입니다.

## 구현 내용

- `TfidfVectorizer`로 질문과 후보 답변 벡터화
- 질문과 답변 간 Cosine Similarity를 이용한 Relevance 비교
- Ground Truth와 생성 답변의 유사도를 이용한 Correctness 개념 실습

## 파일

- `real.py` : TF-IDF + Cosine Similarity를 이용한 간단한 Relevance/Correctness 계산

이 실습은 실제 RAG 평가 지표를 완성한 구현이라기보다, 검색 결과와 생성 답변을 별도로 평가해야 하는 이유를 이해하기 위한 기초 실습입니다.
