from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import settings
from app.models import User, Product
from app.routers import auth
from app.routers import product

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for monitoring product prices across various e-commerce platforms."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(product.router)

@app.get("/")
def read_root():
    return {"message": "Price Monitor is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}