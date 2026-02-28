from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    url = Column(String(255), nullable=False)
    price = Column(Float, nullable=True)
    target_price = Column(Float, nullable=False)
    minor_price = Column(Float, nullable=True)
    last_checked = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="products")