from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas import UserCreate, UserLogin, Token, User as UserSchema
from app.services import user_service
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.register(db, user)
    
    

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return user_service.login(db, user)

@router.get("/me", response_model= UserSchema)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user