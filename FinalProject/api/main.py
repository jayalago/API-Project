import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
import models
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func
# all of the new imports are from python project 2
# that's what i'm using as a reference


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

db_dependency = Annotated[Session, Depends(get_db)] #needs to be fixed, unsure how

if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)

# do we even need this???? i'm so fucking confused bro - Bella
class MenuBase(BaseModel):
    id: int
    sandwich_id: int
    resource_id: int
    amount: int

class SandwichBase(BaseModel):
    id: int
    sandwich_name: str
    price: float

# if we do end up needing the base models, more will go here

# MENU
@app.get("/menu/", status_code=status.HTTP_200_OK)
async def get_menu(db: db_dependency):
    # return the recipes database

@app.post("/menu/", status_code = status.HTTP_201_CREATED)
async def add_menu_item(): #insert stuff inside parenthesis
    #exactly as it sounds, add a recipe to the recipe database
    return {"detail": "Item added successfully."}

@app.put("/menu/{menu_id}", response_model = MenuBase, status_code=status.HTTP_200_OK )
async def update_menu_item(menu_id: int): # more goes in the parenthesis
    #stuff goes here
    return {"detail": "Item updated successfully."}

@app.delete("/menu/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item(menu_id: int): #more goes inside parenthesis
    #stuff goes here
    return {"detail": "Item deleted successfully."}