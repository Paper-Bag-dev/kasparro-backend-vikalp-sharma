from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CsvCoinItem(BaseModel):
    id: str
    name: str
    symbol: str
    price: Optional[float]
    market_cap: Optional[float]
    volume_24h: Optional[float]
    last_updated: Optional[datetime]

    class Config:
        extra = "allow"
