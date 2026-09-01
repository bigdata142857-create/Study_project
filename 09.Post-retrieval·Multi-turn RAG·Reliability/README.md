# Post-retrieval & RAG Reliability

Retriever가 반환한 결과를 그대로 LLM에 전달하지 않고, 검색 이후 단계에서 Context 품질을 높이는 방법을 학습한 실습입니다.

## 학습 주제

- Relevance 기반 Filtering
- 중복 Chunk 제거(Deduplication)
- 유사 결과 정리 및 Clustering 관점
- 검색 결과를 최종 Context로 구성하기 전 품질을 확인하는 과정

## 파일

- `Post-retrieval Filtering·Deduplication·Clustering.ipynb` : 검색 이후 결과를 정제하는 과정을 단계별로 실습한 Notebook

RAG 품질은 Retriever의 Top-k 결과만으로 결정되지 않으며, 검색 이후 어떤 문서를 남기고 제거할지 역시 중요한 단계라는 점을 확인하는 데 목적을 두었습니다.
