from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
from sqlalchemy import CheckConstraint


class Rating(Base):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_text = Column(String(250), default = "No review provided.")
    score = Column(Integer, CheckConstraint('score BETWEEN 1 AND 5'))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    menu_item_id = Column(Integer, ForeignKey("menu.id"))

    customer = relationship("Customer", back_populates="ratings")
    menu = relationship("Menu", back_populates="ratings")
