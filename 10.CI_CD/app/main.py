import os

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

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


def _save_item(item_id: int, item: dict) -> None:
    """저장 실패 상황을 테스트할 수 있도록 저장 동작을 분리한다."""
    db[item_id] = item


@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(item: ItemIn) -> dict:
    global _next_id

    try:
        new_item = {"id": _next_id, **item.model_dump()}
        _save_item(_next_id, new_item)
        _next_id += 1
        return new_item
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail="failed to save item") from exc


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int) -> dict:
    item = db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    return item


class ChatIn(BaseModel):
    message: str


LLM_API_URL = "https://api.example-llm.com/v1/chat"


@app.post("/chat")
async def chat(payload: ChatIn) -> dict:
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
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
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="LLM API timeout") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"LLM API error: {exc}") from exc


@app.get("/health")
def health() -> dict:
    if not os.environ.get("LLM_API_KEY"):
        raise HTTPException(status_code=503, detail="unhealthy: missing LLM_API_KEY")
    return {"status": "ok"}
