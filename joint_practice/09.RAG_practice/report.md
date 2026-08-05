# RAG Pipeline Report

생성 시간 : 2026-08-04 16:07:51.678970

## Query Rewrite 결과

|현재 질문|Rewrite 결과|
|---|---|
|나머지도 추측해서 작성해줘.|B 방식(Kubernetes)의 운영 배포 절차 전체|

## Post-retrieval 결과표

|단계|Chunk 개수|Token 수|
|---|---:|---:|
|Retrieval|1|11|
|Filtering|1|11|
|Deduplication|1|11|
|Compression|1|11|

## Filtering 결과

제거된 Chunk 없음

## Context 구성표

- B 방식(Kubernetes)의 운영 배포 절차는 다음과 같습니다. 1. Docker Image 생성

## Grounding 결과

|문서|결과|
|---|---|
|deploy.pdf|O|

## Citation

- deploy.pdf

## Guardrail 결과

차단

## Memory 정책

|항목|내용|
|---|---|
|저장된 대화 수|4|
|Rewrite 사용|O|
|대화 요약|X|

## Adaptive Retrieval 정책

운영 배포 절차를 확인하기 위해 외부 문서 검색 수행

## 실패 분석

- 검색 결과가 일부만 존재
- 추측 요청으로 생성 거부

## 최종 답변

B 방식(Kubernetes)의 운영 배포 절차는 다음과 같습니다. 1. Docker Image 생성


출처
- deploy.pdf
