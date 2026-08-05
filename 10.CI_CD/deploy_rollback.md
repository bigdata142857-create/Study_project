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
