from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))

    card_information = Column(String(4), default = 'Null')
    isTransactionComplete = Column(Boolean, default=False)
    payment_type = Column(String(100))
    amount = Column(DECIMAL(10,2))
    #Relationships =======================================================================
    customer = relationship("Customer", back_populates="payments")
    order_details = relationship("order_details", back_populates="payments")
