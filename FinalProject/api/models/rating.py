from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Rating(Base):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_text = Column(String(250))
    score = Column(Integer)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    # rating connected to the customer; unsure if I need to do the backpopulates thing here?
    customer = relationship("Customer", back_populates="ratings")
