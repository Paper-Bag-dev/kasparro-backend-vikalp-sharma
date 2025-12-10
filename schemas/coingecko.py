from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CoinGeckoItem(BaseModel):
    id: str
    symbol: str
    name: str

    current_price: Optional[float] = None
    market_cap: Optional[float] = None
    total_volume: Optional[float] = None

    last_updated: Optional[datetime] = None

    class Config:
        extra = "allow" 
