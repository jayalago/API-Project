from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
'''
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
'''
#Customer
class CustomerBase(BaseModel):
    name: str
    email: str
    phone_number: str
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class Customer(CustomerBase):
    id: int

    class ConfigDict:
        from_attributes = True

#Menu
class MenuBase(BaseModel):
    #sandwich_id: int
    #resource_id: int
    item_name: str
    item_ingredients: str
    price: float
    isVegetarian: bool

class MenuCreate(MenuBase):
    pass

class MenuUpdate(BaseModel):
    item_name: Optional[str]
    item_ingredients: Optional[str]
    price: Optional[float] = None
    isVegetarian: Optional[bool] = None

class Menu(MenuBase):
    id: int

    class ConfigDict:
        from_attributes = True
'''
#Order details
class OrderDetailBase(BaseModel):
    order_id: int
    sandwich_id: int
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
    sandwich: Optional[Sandwich]

    class ConfigDict:
        from_attributes = True
        '''

#Orders
class OrderBase(BaseModel):
    #id: int
    customer_id: int
    menu_item_id: int
    quantity: int
    order_status: Optional[str] = "Order not in progress"
    total_price: Optional[float] = 0.00
    promo_code: Optional[str] = None


class OrderCreate(OrderBase):
    # order_details: Optional[list[OrderDetail]] = None
    pass

class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    menu_id: Optional[int] = None
    quantity: Optional[int] = None
    order_status: Optional[str] = None
    total_price: Optional[float] = None
    promo_code: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: datetime

    class Config:
        from_attributes = True

#Payment
class PaymentBase(BaseModel):
    customer_id: int
    order_id: int
    card_information: str
    payment_type: str
    amount: float
    isTransactionComplete: Optional[bool] = False


class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    customer_id: Optional[int] = None
    order_id: Optional[int] = None
    card_information: Optional[str] = None
    payment_type: Optional[str] = None
    amount: Optional[float] = None
    isTransactionComplete: Optional[bool] = None

class Payment(PaymentBase):
    id: int

    class ConfigDict:
        from_attributes = True

#Promotion
class PromotionBase(BaseModel):
    promo_code: str
    expiration_date: Optional[datetime] = None
    discount: float

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    promo_code: Optional[str] = None
    expiration_date: Optional[datetime] = None
    discount: Optional[float] = None

class Promotion(PromotionBase):
    class ConfigDict:
        from_attributes = True

#Rating
class RatingBase(BaseModel):
    review_text: Optional[str] = None
    score: int
    customer_id: int
    menu_id: int

class RatingCreate(RatingBase):
    pass

class RatingUpdate(BaseModel):
    review_text: Optional[str] = None
    score: Optional[int] = None
    customer_id: Optional[int] = None
    menu_id: Optional[int] = None

class Rating(RatingBase):
    id: int

    class ConfigDict:
        from_attributes = True

#Recipes
class RecipesBase(BaseModel):
    amount: int

class RecipesCreate(RecipesBase):
    menu_id: int
    resource_id: int

class RecipesUpdate(BaseModel):
    menu_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[int] = None

class Recipes(RecipesBase):
    id: int
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