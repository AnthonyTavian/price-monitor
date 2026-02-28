from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import ProductCreate, Product as ProductSchema, ProductUpdate
from app.utils.dependencies import get_current_user
from app.services import product_service

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return product_service.create_product(db, product, current_user.id)

@router.get("", response_model=List[ProductSchema])
def get_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = Query(None, description="Filter by product name"),
    url: Optional[str] = Query(None, description="Filter by product URL"),
    current_user = Depends(get_current_user)
):
    return product_service.get_products(db, current_user.id, skip, limit, name, url)


@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return product_service.get_product(db, product_id, current_user.id)

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return product_service.update_product(product_id, product, db, current_user.id)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return product_service.delete_product(product_id, db, current_user.id)