from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .sandwiches import Sandwich


class OrderDetailBase(BaseModel):
    customer_name: str
    order_status: Optional[str] = "Order not in progress"
    total_price: Optional[float] = 0.00


class OrderDetailCreate(OrderDetailBase):
    order_id: int
    sandwich_id: int

class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    sandwich_id: Optional[int] = None
    amount: Optional[int] = None


class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    sandwich: Sandwich = None
    order_date: datetime

    class ConfigDict:
        from_attributes = True