from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = 'promotions'

    promo_code = Column(String(100), primary_key=True)
    expiration_date = Column(DATETIME)
    discount = Column(DECIMAL, default=0.00)

    orders = relationship("Order", back_populates="promotion")
