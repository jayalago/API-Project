import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .dependencies.database import engine, SessionLocal, get_db
from .models import model_loader
from .dependencies.config import conf
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func
from .schemas import schema
from .models import customer, menu, payment, promotion, rating, recipes, orders

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
@app.get("/menu/", status_code=status.HTTP_200_OK)
async def get_menu(db: db_dependency):
   return db.query(menu.Menu).all() # menu.Menu is equivalent to model.class, just specifying which file in the model file to use

@app.post("/menu/", status_code = status.HTTP_201_CREATED)
async def add_menu_item(Menu: schema.MenuBase, db: db_dependency):
    db_menu = menu.Menu(**Menu.model_dump()) #lowercase menu is the menu.py file, uppercase is the parameter for the function
    db.add(db_menu)
    db.commit()
    return {"detail": "Item added successfully."}

@app.put("/menu/{menu_id}", response_model = schema.MenuBase, status_code=status.HTTP_200_OK )
async def update_menu_item(menu_id: int, menu_request: schema.MenuBase, db: db_dependency): # more goes in the parenthesis
    db_menu = db.query(menu.Menu).filter(menu.Menu.id == menu_id)
    if db_menu.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    update_data = menu_request.model_dump(exclude_unset = True)
    db_menu.update(update_data, synchronize_session=False)
    db.commit()
    print("Item updated successfully.")
    return db_menu.first()


@app.delete("/menu/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item(menu_id: int, menu_request: schema.MenuBase, db: db_dependency): #more goes inside parenthesis
    db_menu = db.query(menu.Menu).filter(menu.Menu.id == menu_id)
    if db_menu.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    delete_data = menu_request.model_dump(exclude_unset = True)
    db_menu.delete(delete_data)
    db.commit()
    return {"detail": "Item deleted successfully."}

# Orders ============================================================================================
@app.get("/orders/", status_code=status.HTTP_200_OK)
async def get_all_orders(db: db_dependency):
   return db.query(orders.Order).all()

@app.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
async def get_order(order_id: int, db: db_dependency):
    db_order = db.query(orders.Order).filter(orders.Order.id == order_id)
    if db_order.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return db_order.first()

@app.post("/orders/", status_code=status.HTTP_201_CREATED)
async def add_new_order(Orders: schema.OrderBase, db: db_dependency):
    db_orders = orders.Order(**Orders.model_dump())
    db.add(db_orders)
    db.commit()
    return {"detail": "Order created successfully."}

@app.put("/order/{order_id}", response_model = schema.OrderBase, status_code=status.HTTP_200_OK )
async def update_order(order_id: int, order_request: schema.OrderUpdate, db: db_dependency): # more goes in the parenthesis
    db_order = db.query(orders.Order).filter(orders.Order.id == order_id)
    if db_order.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    update_data = order_request.model_dump(exclude_unset = True)
    db_order.update(update_data, synchronize_session=False)
    db.commit()
    print("Order updated successfully.")
    return db_order.first()

@app.delete("/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, order_request: schema.OrderBase, db: db_dependency): #more goes inside parenthesis
    db_order = db.query(orders.Order).filter(orders.Order.id == order_id)
    if db_order.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    delete_data = order_request.model_dump(exclude_unset = True)
    db_order.delete(delete_data)
    db.commit()
    return {"detail": "Order deleted successfully."}


# Customers ================================================================================================
@app.get("/customers/", status_code=status.HTTP_200_OK)
async def get_all_customers(db: db_dependency):
    return db.query(customer.Customer).all()

@app.get("/customers/{customer_id}", status_code=status.HTTP_200_OK)
async def get_customer(customer_id: int, db: db_dependency):
    db_customer = db.query(customer.Customer).filter(customer.Customer.id == customer_id)
    if db_customer.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return db_customer.first()

@app.post("/customers/", status_code=status.HTTP_201_CREATED)
async def add_new_customer(customer_data: schema.CustomerBase, db: db_dependency):
    db_customer =  customer.Customer(**customer_data.model_dump())
    db.add(db_customer)
    db.commit()
    return {"detail": "Customer created successfully."}

@app.put("/customers/{customer_id}", response_model=schema.CustomerBase, status_code=status.HTTP_200_OK )
async def update_customer(customer_id: int, customer_request: schema.CustomerUpdate, db: db_dependency):
    db_customer = db.query(customer.Customer).filter(customer.Customer.id == customer_id)
    if db_customer.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    update_data = customer_request.model_dump(exclude_unset = True)
    db_customer.update(update_data, synchronize_session=False)
    db.commit()
    print("Customer updated successfully.")
    return db_customer.first()

@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, db: db_dependency):
    db_customer = db.query(customer.Customer).filter(customer.Customer.id == customer_id)
    if db_customer.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    db_customer.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Customer deleted successfully."}
#