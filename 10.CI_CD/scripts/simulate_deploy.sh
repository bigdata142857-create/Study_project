#!/bin/bash
# 배포 -> Health Check 실패 -> 신규 버전 중단 -> 이전 버전 유지 -> 로그 확인
# 을 로컬에서 흉내내는 시뮬레이션 스크립트
#
# 사용법: "10.CI_CD" 폴더(app 폴더가 있는 곳)에서 실행
#   cd 10.CI_CD
#   chmod +x scripts/simulate_deploy.sh
#   ./scripts/simulate_deploy.sh

set -uo pipefail

LOG_FILE="deploy.log"
V1_PORT=8000
V2_PORT=8001

echo "=== 배포 시뮬레이션 시작: $(date) ===" | tee -a "$LOG_FILE"

# 1. 이전 버전(v1) 실행 - 환경변수를 정상적으로 설정한 상태
echo "[1] 이전 버전(v1, port=$V1_PORT) 실행 중..." | tee -a "$LOG_FILE"
LLM_API_KEY=dummy-key uvicorn app.main:app --port $V1_PORT > v1.log 2>&1 &
V1_PID=$!
sleep 2

# 2. 신규 버전(v2) 배포 - 일부러 환경변수를 빼서 배포 (실제 실수 상황을 재현)
echo "[2] 신규 버전(v2, port=$V2_PORT) 배포 중... (환경변수 누락 상태로 배포)" | tee -a "$LOG_FILE"
uvicorn app.main:app --port $V2_PORT > v2.log 2>&1 &
V2_PID=$!
sleep 2

# 3. Health Check
echo "[3] 신규 버전 Health Check 요청 중..." | tee -a "$LOG_FILE"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$V2_PORT/health)
echo "    -> 응답 코드: $STATUS" | tee -a "$LOG_FILE"

if [ "$STATUS" == "200" ]; then
    echo "[4] Health Check 성공. 신규 버전으로 트래픽 전환 (배포 완료)." | tee -a "$LOG_FILE"
    echo "    이전 버전(v1, port=$V1_PORT) 종료." | tee -a "$LOG_FILE"
    kill "$V1_PID" 2>/dev/null
else
    echo "[4] Health Check 실패 (status=$STATUS). 신규 버전 중단." | tee -a "$LOG_FILE"
    kill "$V2_PID" 2>/dev/null

    echo "[5] 이전 버전(v1, port=$V1_PORT) 유지 상태 확인 중..." | tee -a "$LOG_FILE"
    V1_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$V1_PORT/health)
    echo "    -> v1 상태: $V1_STATUS (계속 서비스 중)" | tee -a "$LOG_FILE"

    echo "[6] 실패 원인 로그(v2.log) 확인:" | tee -a "$LOG_FILE"
    tail -n 5 v2.log | tee -a "$LOG_FILE"
fi

echo "=== 배포 시뮬레이션 종료: $(date) ===" | tee -a "$LOG_FILE"
echo ""
echo "전체 로그는 deploy.log, v1.log, v2.log 파일에서 확인할 수 있습니다."