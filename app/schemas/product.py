from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    url: str
    target_price: float

class Product(BaseModel):
    id: int
    url: str
    name: Optional[str] = None
    price: Optional[float] = None
    target_price: float
    minor_price: Optional[float] = None
    last_checked: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    url: Optional[str] = None
    target_price: Optional[float] = None