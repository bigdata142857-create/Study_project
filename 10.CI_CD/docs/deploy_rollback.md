# 배포 / Rollback 학습 정리

## 1. 코드 품질 검사 명령 (로컬)

| 목적 | 도구 | 명령 |
|---|---|---|
| Formatter 검사 | black | `black --check .` |
| Formatter 자동 정리 | black | `black .` |
| Lint | ruff | `ruff check .` |
| Type Check | mypy | `mypy app` |
| 테스트 실행 | pytest | `pytest -v` |

CI에서는 위 명령을 순서대로 실행하고, 하나라도 실패(exit code != 0)하면
워크플로우가 중단되고 job이 실패 상태가 된다. 이 job을 브랜치 보호 규칙의
Required status check로 지정하면 실패 시 Merge 버튼이 비활성화된다.

## 2. 개발 / 테스트 / 운영 환경 비교

| 항목 | 개발(dev) | 테스트(staging/test) | 운영(prod) |
|---|---|---|---|
| 목적 | 기능 개발, 빠른 반복 | 배포 전 최종 검증 | 실제 사용자 서비스 |
| 데이터 | 가짜/샘플 데이터 | 운영과 유사한 데이터 (마스킹) | 실제 데이터 |
| 배포 빈도 | 매우 잦음 | PR merge마다 | 릴리스 단위 |
| 비밀정보 관리 | 로컬 `.env` (커밋 금지) | CI/CD Secret (예: GitHub Actions Secrets) | Secret Manager / Vault, 최소 권한 원칙 |
| 외부 API | Mock 또는 Sandbox 키 | Sandbox 또는 제한된 실키 | 실제 Production 키 |
| 모니터링 | 최소 | 배포 검증용 로그 확인 | Alerting, Health Check, 대시보드 상시 운영 |
| Rollback 필요성 | 낮음 | 중간 | 필수 (즉시 대응) |

환경별로 같은 코드가 실행되지만 `.env` 파일이나 CI/CD Secret으로 값만 바꿔
주입한다 (예: `LLM_API_KEY`, `DATABASE_URL`). 코드에 환경별 분기(`if env == "prod"`)를
최대한 넣지 않는 것이 원칙이다.

## 3. 배포 & Rollback 흐름도

```
[신규 버전 빌드]
      │
      ▼
[신규 버전 배포 (예: Blue/Green 중 Green 슬롯)]
      │
      ▼
[DB Migration 적용]
      │
      ▼
[Health Check 요청 (/health)]
      │
      ├── 성공 ──▶ [트래픽을 신규 버전으로 전환] ──▶ [배포 완료, 로그/모니터링 계속 관찰]
      │
      └── 실패 ──▶ [신규 버전 트래픽 차단 / 중단]
                        │
                        ▼
                  [이전 버전(Blue 슬롯) 재실행 유지]
                        │
                        ▼
                  [실패 로그 확인 및 원인 분석]
                        │
                        ▼
                  [원인 수정 후 재배포 시도]
```

핵심 원칙:
- 신규 버전은 Health Check를 통과하기 전까지 실제 트래픽을 받지 않는다.
- 이전 버전은 신규 버전이 검증되기 전까지 내려가지 않는다 (즉시 Rollback 가능해야 함).
- Rollback은 "코드를 되돌리는 것"이 아니라 "트래픽을 이전에 검증된 버전으로 다시 돌리는 것"이 1차 대응이다.

## 4. 실패한 CI 로그 분석 예시

아래는 CI에서 발생할 수 있는 실패 로그 예시와 분석 방법이다.

```
Run pytest -v
...
FAILED app/test_main.py::test_chat_missing_env - assert 200 == 500
============================== 1 failed, 6 passed in 0.42s ===============================
Error: Process completed with exit code 1.
```

분석 순서:
1. **어느 단계에서 실패했는가** — 로그 상단의 step 이름(`Run tests (pytest)`)으로 Formatter/Lint/Type Check/Test 중 어디서 막혔는지 먼저 확인한다.
2. **어떤 테스트가 실패했는가** — `FAILED app/test_main.py::test_chat_missing_env`에서 실패한 테스트 함수명을 확인한다.
3. **assert 내용 비교** — `assert 200 == 500`은 기대한 응답 코드(500, 환경변수 누락 시 에러)와 실제 응답 코드(200)가 다르다는 뜻 → 코드가 환경변수 누락을 제대로 감지하지 못하고 있다는 신호.
4. **재현** — 로컬에서 동일 명령(`pytest -v -k test_chat_missing_env`)을 실행해 같은 결과가 나오는지 확인.
5. **원인 특정 후 수정** — 예: `os.environ.get` 대신 캐싱된 설정 객체를 참조해서 monkeypatch가 반영되지 않는 경우 등.

## 5. 배포 성공 / 실패 판단 기준 (예시)

- Build 성공 여부 (exit code)
- DB Migration 적용 성공 여부
- `/health` 응답이 200을 반환하는지, 지정된 timeout(예: 30초) 내에 응답하는지
- 신규 버전 배포 직후 일정 시간(예: 5분) 동안 에러율/응답 지연이 임계치를 넘지 않는지

위 조건 중 하나라도 실패하면 자동으로 Rollback을 트리거하고, 담당자에게 알림을 보낸다.

## 6. 의도적으로 오류를 재현하고 로그 확인하기 (공통 실습 4~5단계)

먼저 서버를 로컬에서 띄웁니다 (레포 루트에서):

```bash
LLM_API_KEY=dummy-key uvicorn app.main:app --reload
```

그 다음 아래 요청들을 하나씩 보내면서, 터미널에 찍히는 로그(그리고 실패 시 traceback)를 직접 확인합니다.

| 시나리오 | 명령 |
|---|---|
| 정상 요청 | `curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d "{\"name\":\"apple\",\"price\":1000}"` |
| 입력값 검증 실패 | `curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d "{\"name\":\"apple\",\"price\":-100}"` |
| 데이터 없음 | `curl http://localhost:8000/items/999` |
| 환경변수 누락 | 서버를 `LLM_API_KEY` 없이 다시 띄운 뒤 `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"hi\"}"` |
| Health Check 실패 | 위와 동일하게 환경변수 없이 띄운 뒤 `curl http://localhost:8000/health` |

각 요청 후 터미널(uvicorn 실행 창)에 찍히는 로그 줄을 보고:
- 어떤 레벨(INFO/WARNING/ERROR)로 찍혔는지
- (DB 저장 실패, LLM Timeout처럼 `logger.exception`을 쓴 경우) traceback이 몇 줄짜리로 나오는지, 어느 파일의 몇 번째 줄에서 예외가 발생했다고 나오는지
를 확인하는 게 "로그와 Traceback 분석" 실습입니다.

## 7. SSH로 원격 서버 상태 확인하기 (공통 실습 6단계)

실제 배포된 원격 서버(클라우드 VM 등)가 있다면 다음과 같은 명령으로 상태를 확인합니다:

```bash
ssh <user>@<server-ip>
ps aux | grep uvicorn        # 프로세스가 살아있는지 확인
curl http://localhost:8000/health   # 서버 내부에서 직접 health check
tail -n 50 /path/to/app.log  # 최근 로그 확인
```

만약 아직 원격 서버가 없다면, 개념만 익혀두고 나중에 실제 배포 시(예: AWS 프리티어 EC2) 그대로 적용하면 됩니다. 지금 로컬에서 미리 연습해보고 싶다면, 본인 PC에 OpenSSH 서버를 설치해서 `ssh localhost`로 접속해보고 위 명령들을 그대로 실습해볼 수도 있습니다.

## 8. 배포·Rollback을 직접 실행해보기

`scripts/simulate_deploy.sh`를 실행하면 지금까지 문서로만 정리했던 흐름을 실제로 실행해볼 수 있습니다.

```bash
chmod +x scripts/simulate_deploy.sh
./scripts/simulate_deploy.sh
```

이 스크립트는:
1. 이전 버전(v1)을 정상 설정으로 실행
2. 신규 버전(v2)을 **일부러 환경변수 없이** 배포 (실수 상황 재현)
3. v2에 Health Check 요청 → 503 실패 확인
4. v2를 종료(신규 버전 중단)하고 v1이 계속 살아있는지 확인
5. `v2.log`에서 실패 원인(로그) 확인
6. 전체 과정을 `deploy.log`에 기록

실행 후 `deploy.log`, `v1.log`, `v2.log` 세 파일을 열어보면 "배포 실패 → 로그 확인" 흐름을 그대로 볼 수 있습니다.