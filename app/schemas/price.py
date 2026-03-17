from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PriceBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=50)
    price_usd: float = Field(..., gt=0)
    change_24h: Optional[float] = None
    market_cap: Optional[float] = None
    volume_24h: Optional[float] = None


class PriceResponse(PriceBase):
    id: int
    recorded_at: datetime

    model_config = {"from_attributes": True}


class PriceHistoryResponse(BaseModel):
    symbol: str
    prices: list[PriceResponse]
    total: int


class SentimentResponse(BaseModel):
    symbol: str
    label: str
    score: float = Field(..., ge=0, le=1)
    headlines_analyzed: int