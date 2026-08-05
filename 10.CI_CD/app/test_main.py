from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi.testclient import TestClient

from main import app, db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """각 테스트 전후로 인메모리 DB를 초기화한다."""
    db.clear()
    yield
    db.clear()


@pytest.fixture
def llm_api_key(monkeypatch):
    """LLM_API_KEY 환경변수가 설정된 상태를 만드는 Fixture."""
    monkeypatch.setenv("LLM_API_KEY", "test-key")


# 1. 정상 API 요청
def test_create_item_success():
    res = client.post("/items", json={"name": "apple", "price": 1000})
    assert res.status_code == 201
    assert res.json()["name"] == "apple"


# 2. 입력값 검증 실패
def test_create_item_invalid_price():
    res = client.post("/items", json={"name": "apple", "price": -100})
    assert res.status_code == 422


# 3. 데이터가 존재하지 않음
def test_get_item_not_found():
    res = client.get("/items/999")
    assert res.status_code == 404


# 4. DB 저장 실패 (Mock으로 강제 발생)
def test_create_item_db_failure(monkeypatch):
    def broken_setitem(key, value):
        raise RuntimeError("db down")

    monkeypatch.setattr(db, "__setitem__", broken_setitem)
    res = client.post("/items", json={"name": "apple", "price": 1000})
    assert res.status_code == 500


# 5. 외부 LLM API Timeout
def test_chat_timeout(llm_api_key):
    with patch(
        "httpx.AsyncClient.post",
        new=AsyncMock(side_effect=httpx.TimeoutException("timeout")),
    ):
        res = client.post("/chat", json={"message": "hi"})
    assert res.status_code == 504


# 6. 환경변수 누락
def test_chat_missing_env(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    res = client.post("/chat", json={"message": "hi"})
    assert res.status_code == 500


# 7. 서버 Health Check 실패 / 성공
def test_health_check_fail(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    res = client.get("/health")
    assert res.status_code == 503


def test_health_check_ok(llm_api_key):
    res = client.get("/health")
    assert res.status_code == 200
