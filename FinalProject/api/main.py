import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .dependencies.database import engine, SessionLocal, get_db
from .dependencies.config import conf
from pydantic import BaseModel
from typing import Annotated, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from .schemas import schema
from .models import model_loader, customer, menu, payment, promotion, rating, recipes, orders

app = FastAPI()

db_dependency = Annotated[Session, Depends(get_db)]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()

if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)

# I think once the Menu schema is completed, this will work better
# Menu =====================================================================================================
@app.get("/menu/", response_model=List[schema.Menu], tags=["Menu"])
async def get_menu(db: db_dependency):
   return db.query(menu.Menu).all() # menu.Menu is equivalent to model.class, just specifying which file in the model file to use

@app.get("/menu/vegetarian", status_code=status.HTTP_200_OK, tags=["Menu"])
async def get_vegetarian_menu(db: db_dependency):
    return db.query(menu.Menu).filter(menu.Menu.isVegetarian == True).all()


@app.post("/menu/", status_code=status.HTTP_201_CREATED, tags=["Menu"])
async def add_menu_item(menu_request: schema.MenuCreate, db: db_dependency):
    db_menu = menu.Menu(**menu_request.model_dump()) #lowercase menu is the menu.py file, uppercase is the parameter for the function
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    #return {"detail": "Item added successfully."}
    return db_menu

@app.put("/menu/{menu_id}", response_model = schema.MenuUpdate, status_code=status.HTTP_200_OK, tags=["Menu"])
async def update_menu_item(menu_id: int, menu_request: schema.MenuUpdate, db: db_dependency): # more goes in the parenthesis
    db_menu = db.query(menu.Menu).filter(menu.Menu.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    update_data = menu_request.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_menu, key, value)
    #db_menu.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_menu)
    #print("Item updated successfully.")
    return db_menu


@app.delete("/menu/{menu_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Menu"])
async def delete_menu_item(menu_id: int, db: db_dependency): #more goes inside parenthesis
    db_menu = db.query(menu.Menu).filter(menu.Menu.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    #delete_data = menu_request.model_dump(exclude_unset = True)
    #db_menu.delete(delete_data)
    db.delete(db_menu)
    db.commit()
    return {"detail": "Item deleted successfully."}

# Orders ============================================================================================
@app.get("/orders/", status_code=status.HTTP_200_OK, tags=["Orders"])
async def get_all_orders(db: db_dependency):
   return db.query(orders.Order).all()

#This reveals all order details
@app.get("/orders/{tracking_number}", status_code=status.HTTP_200_OK, tags=["Orders"])
async def track_order(tracking_number: int, db: db_dependency):
    db_order = db.query(orders.Order).filter(orders.Order.id == tracking_number).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "tracking_number": db_order.id,
        "status": db_order.order_status,
        "order_date": db_order.order_date,
        "is_takeout": db_order.isTakeout,
        "is_delivery": db_order.isDelivery,
        "total_price": db_order.total_price
    }

#Reveals all orders in specific time frame
@app.get("/orders/{date_range}", status_code=status.HTTP_200_OK, tags=["Orders"])
async def get_orders_by_date_range(start_date: str, end_date: str, db: db_dependency):
    return db.query(orders.Order).filter(
        orders.Order.order_date >= start_date,
        orders.Order.order_date <= end_date
    ).all()
#shows payment to order
@app.post("/orders/{order_id}/pay", tags=["Orders"])
async def pay_order(order_id: int, payment_data: schema.PaymentCreate, db: db_dependency):
    order = db.query(orders.Order).get(order_id)
    if payment_data.amount >= float(payment.order.total_price):
        payment.isTransactionComplete = True
        db.commit()
        db.refresh(payment)

    return payment

@app.post("/orders/", status_code=status.HTTP_201_CREATED, tags=["Orders"])
async def add_new_order(order_request: schema.OrderCreate, db: db_dependency):
    db_orders = orders.Order(**order_request.model_dump())
    db.add(db_orders)
    db.commit()
    db.refresh(db_orders)
    return {
        "detail": "Order created successfully.",
        "tracking_number": db_orders.id
            }

@app.put("/order/{order_id}", response_model=schema.OrderBase, status_code=status.HTTP_200_OK, tags=["Orders"])
async def update_order(order_id: int, order_request: schema.OrderUpdate, db: db_dependency): # more goes in the parenthesis
    db_order = db.query(orders.Order).filter(orders.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    update_data = order_request.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    #db_order.update(update_data, synchronize_session=False)
    db.commit()
    print("Order updated successfully.")
    return db_order.first()

#Applying promo
@app.put("/orders/{order_id}/apply-promo", status_code=status.HTTP_200_OK, tags=["Orders"])
async def apply_promo_code(order_id: int, promo_code: str, db: db_dependency):
    order = db.query(orders.Order).filter(orders.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.promo_code = promo_code
    db.commit()
    return order


@app.delete("/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Orders"])
async def delete_order(order_id: int, db: db_dependency): #more goes inside parenthesis
    db_order = db.query(orders.Order).filter(orders.Order.id == order_id)
    if db_order.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    #delete_data = order_request.model_dump(exclude_unset = True)
    db_order.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Order deleted successfully."}



# Customers ================================================================================================
@app.get("/customers/", status_code=status.HTTP_200_OK, tags=["Customers"])
async def get_all_customers(db: db_dependency):
    return db.query(customer.Customer).all()

@app.get("/customers/{customer_id}", status_code=status.HTTP_200_OK, tags=["Customers"])
async def get_customer(customer_id: int, db: db_dependency):
    db_customer = db.query(customer.Customer).filter(customer.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return db_customer

@app.post("/customers/", status_code=status.HTTP_201_CREATED, tags=["Customers"])
async def add_new_customer(customer_data: schema.CustomerCreate, db: db_dependency):
    db_customer =  customer.Customer(**customer_data.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return {
        "detail": "Customer created successfully.",
        "customer_id": db_customer.id
    }

@app.put("/customers/{customer_id}", response_model=schema.Customer, status_code=status.HTTP_200_OK, tags=["Customers"])
async def update_customer(customer_id: int, customer_request: schema.CustomerUpdate, db: db_dependency):
    db_customer = db.query(customer.Customer).filter(customer.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    update_data = customer_request.model_dump(exclude_unset = True)
    #db_customer.update(update_data, synchronize_session=False)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    db.commit()
    #print("Customer updated successfully.")
    return db_customer

@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Customers"])
async def delete_customer(customer_id: int, db: db_dependency):
    db_customer = db.query(customer.Customer).filter(customer.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    db_customer.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Customer deleted successfully."}



# Promotions ================================================================================================
@app.get("/promotions/", status_code=status.HTTP_200_OK, tags=["Promotions"])
async def get_all_promotions(db: db_dependency):
    return db.query(promotion.Promotion).all()

@app.get("/promotions/{promotion_id}", status_code=status.HTTP_200_OK, tags=["Promotions"])
async def get_promotion(promo_code: str, db: db_dependency):
    db_promotion = db.query(promotion.Promotion).filter(promotion.Promotion.promo_code == promo_code).first()
    if db_promotion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
    return db_promotion

@app.post("/promotions/", status_code=status.HTTP_201_CREATED, tags=["Promotions"])
async def add_new_promotion(promotion_request: schema.PromotionCreate, db: db_dependency):
    db_promotion = promotion.Promotion(**promotion_request.model_dump())
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return {"detail": "Promotion created successfully.", "promo_code": db_promotion.promo_code}

@app.put("/promotions/{promo_code}", response_model=schema.Promotion, status_code=status.HTTP_200_OK, tags=["Promotions"])
async def update_promotion(promo_code: str, promotion_request: schema.PromotionUpdate, db: db_dependency):
    db_promotion = db.query(promotion.Promotion).filter(promotion.Promotion.promo_code == promo_code).first()
    if db_promotion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
    update_data = promotion_request.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_promotion, key, value)
    #db_promotion.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_promotion)
    #print("Promotion updated successfully.")
    return db_promotion

@app.delete("/promotions/{promo_code}", status_code=status.HTTP_204_NO_CONTENT, tags=["Promotions"])
async def delete_promotion(promo_code: str, db: db_dependency):
    db_promotion = db.query(promotion.Promotion).filter(promotion.Promotion.promo_code == promo_code).first()
    if db_promotion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
    db.delete(db_promotion)
    db.commit()
    return {"detail": "Promotion deleted successfully."}

# Ratings ================================================================================================
@app.get("/ratings/", status_code=status.HTTP_200_OK, tags=["Ratings"])
async def get_ratings(db: db_dependency):
    return db.query(rating.Rating).all()

@app.get("/ratings/{rating_id}", status_code=status.HTTP_200_OK, tags=["Ratings"])
async def get_rating(rating_id: int, db: db_dependency):
    db_rating = db.query(rating.Rating).filter(rating.Rating.id == rating_id).first()
    if db_rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    return db_rating

@app.post("/ratings/", response_model=schema.Rating, status_code=status.HTTP_200_OK, tags=["Ratings"])
async def add_new_rating(rating_request: schema.RatingCreate, db: db_dependency):
    db_rating = rating.Rating(**rating_request.model_dump())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    #return {"detail": "Rating created successfully."}
    return db_rating

@app.put("/ratings/{rating_id}", response_model=schema.RatingBase, status_code=status.HTTP_200_OK, tags=["Ratings"])
async def update_rating(rating_id: int, rating_request: schema.RatingUpdate, db: db_dependency):
    db_rating = db.query(rating.Rating).filter(rating.Rating.id == rating_id).first()
    if db_rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    update_data = rating_request.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_rating, key, value)
    #db_rating.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_rating)
    #print("Rating updated successfully.")
    return db_rating

@app.delete("/ratings/{rating_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Ratings"])
async def delete_rating(rating_id: int, db: db_dependency):
    db_rating = db.query(rating.Rating).filter(rating.Rating.id == rating_id).first()
    if db_rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    db.delete(db_rating)
    db.commit()
    return {"detail": "Rating deleted successfully."}

#Payment ==========================================================

@app.get("/payments/", status_code=status.HTTP_200_OK, tags=["Payments"])
async def get_all_payments(db: db_dependency):
    return db.query(payment.Payment).all()

@app.get("/payments/{payment_id}", status_code=status.HTTP_200_OK, tags=["Payments"])
async def get_payment(payment_id: int, db: db_dependency):
    db_payment = db.query(payment.Payment).filter(payment.Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return db_payment

@app.post("/payments/", status_code=status.HTTP_201_CREATED, tags=["Payments"])
async def add_new_payment(payment_data: schema.PaymentCreate, db: db_dependency):
    db_payment = payment.Payment(**payment_data.model_dump())
    db.add(db_payment)
    db.commit()
    return {"detail": "Payment created successfully."}

@app.put("/payments/{payment_id}", response_model=schema.Payment, status_code=status.HTTP_200_OK, tags=["Payments"])
async def update_payemnt(payment_id: int, payment_data: schema.PaymentUpdate, db: db_dependency):
    db_payment = db.query(payment.Payment).filter(payment.Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    update_data = payment_data.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_payment, key, value)
    db.commit()
    db.refresh(db_payment)
    return db_payment
@app.delete("payemnts/{payment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Payments"])
async def delete_payment(payment_id: int, db: db_dependency):
    db_payment = db.query(payment.Payment).filter(payment.Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    db.delete(db_payment)
    db.commit()
    return {"detail": "Payment deleted successfully."}








