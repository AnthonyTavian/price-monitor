from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.database import SessionLocal
from app.models.product import Product
from app.schemas import PriceHistoryCreate
from app.services.scraping_service import scrape_amazon_price
from app.services.price_history_service import create_price_history
from app.services import notification_service
import asyncio

scheduler = BackgroundScheduler()

def check_prices():
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        for product in products:
            try:
                loop = asyncio.new_event_loop()
                data = loop.run_until_complete(scrape_amazon_price(product.url))
                loop.close()
                
                product.price = data["price"]
                product.last_checked = datetime.utcnow()
                db.commit()
                
                create_price_history(db, PriceHistoryCreate(
                    product_id=product.id,
                    price=data["price"]
                ))
                
                if product.price <= product.target_price:
                    print(f"ALERTA! {product.name} atingiu o preço alvo: R${product.price}")
                    notification_service.send_telegram_alert(
                        product_name=product.name,
                        current_price=product.price,
                        target_price=product.target_price
                    )
                    
            except Exception as e:
                print(f"Error checking {product.url}: {e}")
    finally:
        db.close()