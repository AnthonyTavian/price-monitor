from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas import ProductCreate, ProductUpdate
from app.services.scraping_service import scrape_amazon_price
from app.services.price_history_service import create_price_history
from app.schemas import PriceHistoryCreate
import asyncio


def create_product(db: Session, product: ProductCreate, user_id: int) -> Product:
    new_product = Product(**product.dict(), user_id=user_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    try:
        loop = asyncio.new_event_loop()
        data = loop.run_until_complete(scrape_amazon_price(new_product.url))
        loop.close()
        new_product.price = data["price"]
        new_product.name = data["name"]
        db.commit()

        create_price_history(db, PriceHistoryCreate(
            product_id=new_product.id,
            price=data["price"]
        ))

        db.refresh(new_product)
    except Exception as e:
        print(f"Scraping failed: {e}")
        raise e
    return new_product


def get_products(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    url: str = None,
):
    query = db.query(Product).filter(Product.user_id == user_id)
    
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if url:
        query = query.filter(Product.url.ilike(f"%{url}%"))
    
    return query.offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int, user_id: int):
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def update_product(product_id: int, product: ProductUpdate, db: Session, user_id: int):
    db_product = db.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(product_id: int, db: Session, user_id: int):
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product)
    db.commit()