from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import settings
from app.models import User, Product
from app.routers import auth, product, price_history
from app.services.scheduler_service import scheduler, check_prices
from apscheduler.triggers.interval import IntervalTrigger

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
app.include_router(price_history.router)

@app.on_event("startup")
def start_scheduler():
    scheduler.add_job(check_prices, IntervalTrigger(hours=settings.CHECK_INTERVAL_HOURS))
    scheduler.start()

@app.on_event("shutdown")
def stop_scheduler():
    scheduler.shutdown()

@app.get("/")
def read_root():
    return {"message": "Price Monitor is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}