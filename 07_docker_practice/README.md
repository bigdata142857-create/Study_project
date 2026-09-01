# FastAPI + PostgreSQL + Docker Compose

FastAPI 애플리케이션과 PostgreSQL을 각각 컨테이너로 실행하고 Docker Compose로 연결한 실습입니다.

## 구성

```text
07_docker_practice/
├── app/
│   ├── Dockerfile
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── requirements.txt
└── docker-compose.yml
```

## 학습 내용

- FastAPI API와 PostgreSQL DB 분리
- SQLAlchemy를 이용한 DB 연결
- Dockerfile로 FastAPI 이미지 생성
- Docker Compose의 `depends_on`, volume, port 설정
- `/health` 엔드포인트와 Docker Health Check 구성
- `/users` POST/GET API로 데이터 저장·조회 실습

## 실행

```bash
docker compose up --build
```

애플리케이션 코드만 구현하는 것에서 끝내지 않고, API와 DB가 컨테이너 환경에서 함께 동작하는 흐름을 확인했습니다.
