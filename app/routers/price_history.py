from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import price_history_service
from app.schemas import PriceHistoryResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/products", tags=["Price History"])

@router.get("/{product_id}/price-history", response_model=list[PriceHistoryResponse])    
def get_price_history(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):  
    return price_history_service.get_price_history(db, product_id, current_user.id)
