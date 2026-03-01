from pydantic import BaseModel
from datetime import datetime

class PriceHistoryResponse(BaseModel):
    id: int
    product_id: int
    price: float
    checked_at: datetime

    class Config:
        from_attributes = True

class PriceHistoryCreate(BaseModel):
    product_id: int
    price: float