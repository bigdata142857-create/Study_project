# RAG Retrieval Evaluation

동일한 문서와 질문을 사용하면서 Retrieval 전략에 따라 검색 결과가 어떻게 달라지는지 비교하기 위한 실습입니다.

## 담당 구현

E팀에서 다음 두 방식을 중심으로 구현했습니다.

- **Parent-Child Retrieval** : 작은 Child Chunk로 검색한 뒤 관련 Parent 문맥을 반환
- **Multi-hop Retrieval** : 한 번의 검색으로 끝내지 않고 중간 정보를 이용해 다음 검색으로 연결

## 데이터 구성

현재 저장소에는 회사 정책·인사·보안·IT 시스템·조직·프로젝트·사내 가이드·회의록·출장 정책으로 구성된 문서와 평가용 파일이 포함되어 있습니다.

```text
08. RAG_평가/
├── documents/
│   ├── 01_company_policy.txt
│   ├── 02_hr_policy.txt
│   ├── 03_security_policy.txt
│   ├── 04_it_system.txt
│   ├── 05_organization.txt
│   ├── 06_project_manual.txt
│   ├── 07_employee_handbook.txt
│   ├── 08_meeting_minutes.txt
│   └── 09_business_trip_policy.txt
├── metadata.csv
├── questions.csv
├── ground_truth.csv
├── parent_child.json
└── document_graph.json
```

## 주요 코드

- `chunking.py` : Parent/Child Chunk 생성
- `embedding.py` : Child Chunk Embedding
- `retrieval.py` : 유사도 기반 검색
- `multi_hop.py` : Multi-hop Retrieval
- `evaluation.py` : 평가 로직
- `main.py` : 전체 실행 흐름

## 학습 포인트

하나의 작은 Chunk만 반환하는 검색과, 검색에 적합한 작은 단위로 찾은 뒤 더 넓은 문맥을 제공하는 방식의 차이를 직접 구현하며 확인했습니다. 또한 여러 문서의 정보가 필요한 질문에서는 검색을 순차적으로 연결하는 방법을 실습했습니다.
