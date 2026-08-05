import logging
import os

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("app")

app = FastAPI()

# 실습용 인메모리 DB
db: dict[int, dict] = {}
_next_id = 1


class ItemIn(BaseModel):
    name: str
    price: float

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("price must be positive")
        return v


class ItemOut(ItemIn):
    id: int


@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(item: ItemIn) -> dict:
    global _next_id
    try:
        new_item = {"id": _next_id, **item.model_dump()}
        db[_next_id] = new_item
        _next_id += 1
        return new_item
    except Exception:
        # 시나리오: DB 저장 실패 -> 전체 traceback을 로그로 남김
        logger.exception("아이템 저장 실패 (item=%s)", item)
        raise HTTPException(status_code=500, detail="failed to save item")


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int) -> dict:
    item = db.get(item_id)
    if item is None:
        # 시나리오: 데이터가 존재하지 않음
        logger.warning("존재하지 않는 아이템 조회 시도: item_id=%s", item_id)
        raise HTTPException(status_code=404, detail="item not found")
    return item


class ChatIn(BaseModel):
    message: str


LLM_API_URL = "https://api.example-llm.com/v1/chat"


@app.post("/chat")
async def chat(payload: ChatIn) -> dict:
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        # 시나리오: 환경변수 누락
        logger.error("LLM_API_KEY 환경변수가 설정되어 있지 않음")
        raise HTTPException(status_code=500, detail="LLM_API_KEY is not set")

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                LLM_API_URL,
                json={"message": payload.message},
                headers={"Authorization": f"Bearer {api_key}"},
            )
            resp.raise_for_status()
            return resp.json()
    except httpx.TimeoutException:
        # 시나리오: 외부 LLM API Timeout -> traceback 포함 로그
        logger.exception("LLM API 호출 timeout 발생")
        raise HTTPException(status_code=504, detail="LLM API timeout")
    except httpx.HTTPStatusError as e:
        logger.exception("LLM API 호출 실패: %s", e)
        raise HTTPException(status_code=502, detail=f"LLM API error: {e}")


@app.get("/health")
def health() -> dict:
    if not os.environ.get("LLM_API_KEY"):
        # 시나리오: 서버 Health Check 실패
        logger.warning("Health check 실패: LLM_API_KEY 환경변수 누락")
        raise HTTPException(status_code=503, detail="unhealthy: missing LLM_API_KEY")
    return {"status": "ok"}
