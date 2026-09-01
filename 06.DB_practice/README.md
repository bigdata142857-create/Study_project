# Database & SQLAlchemy ORM Practice

PostgreSQL과 SQLAlchemy를 연결해 테이블 생성, 데이터 저장, 조회 및 ORM 관계를 학습한 실습입니다.

## 학습 내용

- SQLAlchemy `create_engine`을 이용한 PostgreSQL 연결
- `DeclarativeBase`, `Mapped`, `mapped_column` 기반 ORM 모델 정의
- `Base.metadata.create_all()`을 이용한 테이블 생성
- `Session`을 이용한 Insert/Commit/Select
- 조건 조회 및 모델 분리 실습

## 주요 파일

- `Orm_pr.py` : 하나의 파일에서 User 모델 생성·저장·조회 실습
- `database.py` : Engine/Base 설정
- `models.py` : ORM 모델 정의
- `create_table.py` : 테이블 생성
- `insert_user.py` : 데이터 저장
- `select_user.py` : 데이터 조회

## DB 연결

공개 저장소에 DB 비밀번호를 직접 기록하지 않도록 환경변수에서 연결 URL을 읽도록 구성했습니다.

```bash
# 예시
export ORM_PRACTICE_URL="postgresql://USER:PASSWORD@localhost:5432/orm_practice"
export ORM_PRACTICE2_URL="postgresql://USER:PASSWORD@localhost:5432/orm_practice2"
```

Windows PowerShell에서는 `$env:ORM_PRACTICE_URL="..."` 형식으로 설정할 수 있습니다.
