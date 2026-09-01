# Chunking Practice

RAG에서 문서를 검색 단위로 나누는 여러 Chunking 전략을 직접 구현한 실습입니다.

## 구현한 방식

### Overlap Chunking
- 고정된 Chunk 크기와 Overlap 크기를 지정
- `step = chunk_size - overlap` 방식으로 일부 문장을 다음 Chunk에도 포함

### Recursive Chunking
- 문단 → 줄 → 단어 → 글자 순으로 Separator를 적용
- 최대 길이를 넘는 텍스트만 더 작은 단위로 재귀 분할

### Semantic Chunking
- SentenceTransformer로 각 문장을 임베딩
- 인접 문장의 Cosine Similarity를 계산
- Threshold 이상이면 같은 Chunk로 묶고, 낮으면 새 Chunk 시작

## 파일

- `Overlap.py`
- `Recursive.py`
- `semantic.py`

Chunk 크기만 조절하는 방식과 문서 구조·의미를 활용하는 방식이 Retrieval 결과에 어떤 차이를 만들 수 있는지 이해하는 데 초점을 맞췄습니다.
