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


def test_create_item_success():
    res = client.post("/items", json={"name": "apple", "price": 1000})
    assert res.status_code == 201
    assert res.json()["name"] == "apple"


def test_create_item_invalid_price():
    res = client.post("/items", json={"name": "apple", "price": -100})
    assert res.status_code == 422


def test_get_item_not_found():
    res = client.get("/items/999")
    assert res.status_code == 404


def test_create_item_db_failure():
    with patch("main._save_item", side_effect=RuntimeError("db down")):
        res = client.post("/items", json={"name": "apple", "price": 1000})
    assert res.status_code == 500


def test_chat_timeout(llm_api_key):
    with patch(
        "httpx.AsyncClient.post",
        new=AsyncMock(side_effect=httpx.TimeoutException("timeout")),
    ):
        res = client.post("/chat", json={"message": "hi"})
    assert res.status_code == 504


def test_chat_missing_env(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    res = client.post("/chat", json={"message": "hi"})
    assert res.status_code == 500


def test_health_check_fail(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    res = client.get("/health")
    assert res.status_code == 503


def test_health_check_ok(llm_api_key):
    res = client.get("/health")
    assert res.status_code == 200
