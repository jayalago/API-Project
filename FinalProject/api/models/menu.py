from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

# Originally was called "Recipe"
#Temporarily blocking out the sandwich and resource stuff just for the sake of testing rn
class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    sandwich_name = Column(String(250), nullable=False)
    item_ingredients = Column(String(250), nullable=False)
    isVegetarian = Column(Boolean, default=False)
    price = Column(DECIMAL(3,2), index=True, nullable=False, server_default='0.00')
    # Relationships =======================================================================
    rating = relationship("Rating")
    orders = relationship("Order")
    recipes = relationship("Recipes")