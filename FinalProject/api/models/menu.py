from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

# Originally was called "Recipe"
#Temporarily blocking out the sandwich and resource stuff just for the sake of testing rn
class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(250), nullable=False)
    item_ingredients = Column(String(250), nullable=False)
    isVegetarian = Column(Boolean, default=False)
    price = Column(DECIMAL(3,2), index=True, nullable=False, server_default='0.00')
    # Relationships =======================================================================
    order_details = relationship("order_details", back_populates="menu")

    '''in case yall wanna see what was once sandwiches.py still:
    
    class Sandwich(Base):
    __tablename__ = "sandwiches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_name = Column(String(100), unique=True, nullable=True)
    price = Column(DECIMAL(4, 2), nullable=False, server_default='0.0')

    recipes = relationship("Recipes", back_populates="sandwich") #needs to be changed
    order_details = relationship("OrderDetail", back_populates="sandwich")'''