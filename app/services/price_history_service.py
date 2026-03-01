from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.price_history import PriceHistory
from app.models.product import Product
from app.schemas import PriceHistoryCreate


def create_price_history(db: Session, price_history: PriceHistoryCreate) -> PriceHistory:
    new_price_history = PriceHistory(**price_history.dict())
    db.add(new_price_history)
    db.commit()
    db.refresh(new_price_history)
    return new_price_history

def get_price_history(db: Session, product_id: int, user_id: int):
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    price_histories = db.query(PriceHistory).filter(PriceHistory.product_id == product_id).all()
    if not price_histories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price history not found")
    
    return price_histories