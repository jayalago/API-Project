import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .dependencies.database import engine, SessionLocal, get_db #need to figure out how to import these from the database.py in "dependencies"
from .routers import index as indexRoute
from .models import model_loader
from .schemas import schema
from .dependencies.config import conf
import models
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func
from .schemas import *
from .models import *

'''all of the new imports are from python project 2
# that's what i'm using as a reference
A lot fo these may end up not even being necessary idk'''


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)
models.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)] #needs to be fixed, unsure how

if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)

# I think once the Menu schema is completed, this will work better
# MENU
@app.get("/menu/", status_code=status.HTTP_200_OK)
async def get_menu(db: db_dependency):
   return db.query(models.Menu).all()

@app.post("/menu/", status_code = status.HTTP_201_CREATED)
async def add_menu_item(menu: MenuBase, db: db_dependency):
    db_menu = models.Menu(**todo.model_dump())
    db.add(db_menu)
    db.commit()
    return {"detail": "Item added successfully."}

@app.put("/menu/{menu_id}", response_model = MenuBase, status_code=status.HTTP_200_OK )
async def update_menu_item(menu_id: int): # more goes in the parenthesis
    #stuff goes here
    return {"detail": "Item updated successfully."}

@app.delete("/menu/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item(menu_id: int): #more goes inside parenthesis
    #stuff goes here
    return {"detail": "Item deleted successfully."}

# Orders

# Customers

#