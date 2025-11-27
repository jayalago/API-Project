from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))

    quantity = Column(Integer, default=1)
    total_price = Column(Integer, ForeignKey("total_price.id"))

    # Relationships =======================================================================
    sandwich = relationship("Sandwich", back_populates="order_details")
    order = relationship("Order", back_populates="order_details")












    '''originally in orders.py:
    
    from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_date = Column(DATETIME)
    order_status = Column(String(25), default="Order not in progress")
    total_price = Column(DECIMAL(10,2))

order_details = relationship("OrderDetail", back_populates="order")
customer = relationship("Customer", back_populates="orders")
payments = relationship("Payment", back_populates="orders")
promotion_code = Column(String(250), ForeignKey("promotion.promotion_code"), nullable=True)
promotions = relationship("Promotion", back_populates="orders")'''