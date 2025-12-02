from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
from sqlalchemy import CheckConstraint


class Recipes(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_id = Column(Integer, ForeignKey("menu.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    amount = Column(Integer, index=True, nullable=False, server_default='0.0')

    menu = relationship("Menu")
    resource = relationship("Resource")
