from datetime import datetime
from typing import Optional
from pydantic import BaseModel

#Sandwiches
class SandwichBase(BaseModel):
    sandwich_name: str
    price: float


class SandwichCreate(SandwichBase):
    pass


class SandwichUpdate(BaseModel):
    sandwich_name: Optional[str] = None
    price: Optional[float] = None


class Sandwich(SandwichBase):
    id: int

    class ConfigDict:
        from_attributes = True

#Customer
class CustomerBase(BaseModel):
    pass

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    pass

class Customer(CustomerBase):
    pass

    class ConfigDict:
        from_attributes = True

#Menu
class MenuBase(BaseModel):
    #sandwich_id: int
    #resource_id: int
    item_name: str
    item_ingredients: str
    price: float

class MenuCreate(MenuBase):
    #sandwich_id: Optional[int] = None
    #resource_id: Optional[int] = None
    item_name: Optional[str]
    item_ingredients: Optional[str]
    price: Optional[float] = None

class MenuUpdate(BaseModel):
    pass

class Menu(MenuBase):
    id: int

    class ConfigDict:
        from_attributes = True

#Order details
class OrderDetailBase(BaseModel):
    amount: int


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

    class ConfigDict:
        from_attributes = True

#Orders
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

#Payment
class PaymentBase(BaseModel):
    pass

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    pass

class Payment(PaymentBase):
    pass

    class ConfigDict:
        from_attributes = True

#Promotion
class PromotionBase(BaseModel):
    pass

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    pass

class Promotion(PromotionBase):
    pass

    class ConfigDict:
        from_attributes = True

#Rating
class RatingBase(BaseModel):
    pass

class RatingCreate(RatingBase):
    pass

class RatingUpdate(BaseModel):
    pass

class Rating(RatingBase):
    pass

    class ConfigDict:
        from_attributes = True

#Recipes
class RecipesBase(BaseModel):
    amount: int

class RecipesCreate(RecipesBase):
    sandwich_id: int
    resources_id: int

class RecipesUpdate(BaseModel):
    sandwich_id: Optional[int] = None
    resources_id: Optional[int] = None
    amount: Optional[int] = None

class Recipes(RecipesBase):
    pass

    class ConfigDict:
        from_attributes = True

#Resources
class ResourceBase(BaseModel):
    item: str
    amount: int


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    item: Optional[str] = None
    amount: Optional[int] = None


class Resource(ResourceBase):
    id: int

    class ConfigDict:
        from_attributes = True