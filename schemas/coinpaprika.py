from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class CoinPaprikaItem(BaseModel):
    id: str
    name: str
    symbol: str
    last_updated: Optional[datetime]
    quotes: Dict[str, Any]
    
    class Config:
        extra = "allow"