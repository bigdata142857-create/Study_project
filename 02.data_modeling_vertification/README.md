# Data Modeling & Validation

Python 객체에 데이터를 담는 여러 방식과 Pydantic을 이용한 입력 검증을 비교한 실습입니다.

## 학습 내용

- `dict` 기반 데이터 표현
- `dataclass`를 이용한 구조화된 객체 정의
- Pydantic `BaseModel`을 통한 타입 검증과 변환
- `Enum`, `Optional`을 이용한 입력 범위 및 선택값 표현

## 파일

- `data_modeling.py` : dict, dataclass, Pydantic 비교 실습
- `data_modeling_valid.ipynb` : 데이터 모델링/검증 Notebook

FastAPI 등 API 개발에서 요청·응답 스키마를 정의하기 전에 Python 데이터 모델링 방식의 차이를 확인하는 데 목적을 두었습니다.
