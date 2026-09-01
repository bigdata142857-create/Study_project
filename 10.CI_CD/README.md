# CI/CD Practice

FastAPI 예제에 테스트와 코드 품질 검사를 추가하고 GitHub Actions에서 자동으로 실행하는 CI 실습입니다.

## 실습 API

- `POST /items` : Item 생성 및 입력값 검증
- `GET /items/{item_id}` : Item 조회 / 없는 ID 404 처리
- `POST /chat` : 외부 API Timeout, 환경변수 누락 등 예외 상황 실습
- `GET /health` : 환경변수 상태를 포함한 Health Check

## 자동 검사

`.github/workflows/ci.yml`에서 main push 및 Pull Request 시 다음 순서로 실행합니다.

1. Python 3.12 환경 구성
2. 의존성 설치
3. `black --check`
4. `ruff check`
5. `mypy`
6. `pytest`

## 테스트 시나리오

- 정상 Item 생성
- 잘못된 가격 입력 검증
- 존재하지 않는 ID 조회
- 저장 실패 상황 Mock
- 외부 LLM API Timeout Mock
- API Key 누락
- Health Check 실패/성공

## 배포/롤백 설계

- `deploy_rollback.md` : Blue/Green 배포와 장애 시 Rollback 흐름을 문서로 설계

실패하는 CI를 확인하는 실습에서 끝내지 않고, 실패 원인을 수정해 품질 게이트가 실제로 통과하도록 정리했습니다.
