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
from .models import customer, menu, orders, payment, promotion, rating, recipes

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
# MENU =====================================================================================================
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
@app.post("/order_details/", status_code=status.HTTP_201_CREATED)
async def create_order_details(db: db_dependency):
    db_orderdetails = orders.OrderDetails()
    db.add(db_orderdetails)
    db.commit()
    return {"detail": "Order created successfully."}


# Customers ================================================================================================

#