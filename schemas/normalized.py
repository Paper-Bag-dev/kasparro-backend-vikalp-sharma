from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class NormalizedCoinModel(BaseModel):
    source_name: str
    source_record_id: str
    symbol: Optional[str]
    name: Optional[str]
    price: Optional[float]
    market_cap: Optional[float]
    volume_24h: Optional[float]
    ts: Optional[datetime]
    extra: dict[str, Any] = {}
