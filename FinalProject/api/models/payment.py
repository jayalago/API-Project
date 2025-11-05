from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    card_information = Column(String(100), nullable=False)
    transaction_status = Column(Boolean, default=False) # maybe could be a boolean?
    payment_type = Column(String(100))
    amount = Column(DECIMAL(10,2))

    customer = relationship("Customer", back_populates="payments")
    order = relationship("Order", back_populates="payments")
