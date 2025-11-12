from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

# Originally was called "Recipe"
class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    price = Column(DECIMAL(3,2), index=True, nullable=False, server_default='0.00')

    sandwich = relationship("Sandwich", back_populates="menu")
    resource = relationship("Resource", back_populates="menu")