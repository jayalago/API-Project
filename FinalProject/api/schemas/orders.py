from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail


class OrderBase(BaseModel):
    customer_name: str
    order_status: Optional[str] = "Order not in progress"
    total_price: Optional[float] = 0.00


class OrderCreate(OrderBase):
    order_details: Optional[list[OrderDetail]] = None


class Order(OrderBase):
    id: int
    order_date: datetime

class Config:
        from_attributes = True



'''
class OrderBase(BaseModel):
    customer_name: str
    order_state: Optional[str]
    total_price: Optional[float] = 0.00
    order_date: datetime


class OrderCreate(OrderBase):
    order_details: Optional[list[OrderDetail]] = None


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
'''