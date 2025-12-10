from fastapi import APIRouter, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from core.db import SessionLocal
from core.models import NormalizedCoins

router = APIRouter()

@router.get("/data")
async def get_data(
    request: Request,
    page: int = 1,
    limit: int = 50,
    symbol: str | None = None,
    source: str | None = None
):
    db: Session = SessionLocal()
    query = db.query(NormalizedCoins)

    if symbol:
        query = query.filter(NormalizedCoins.symbol == symbol)
    if source:
        query = query.filter(NormalizedCoins.source_name == source)

    query = query.order_by(
        desc(NormalizedCoins.ingested_at),
        desc(NormalizedCoins.source_name), 
        desc(NormalizedCoins.id),
    )

    items = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "count": len(items),
        "data": [
            {k: v for k, v in item.__dict__.items() if k != "_sa_instance_state"}
            for item in items
        ],
        "metadata": {
            "request_id": request.state.request_id,
            "api_latency_ms": request.headers.get("X-Process-Time-ms")
        },
    }
