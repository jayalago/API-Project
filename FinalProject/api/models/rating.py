from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Rating(Base):
    __tablename__ = "rating"

    review_text = Column(String(250))
    score = Column(Integer)
    customer_name = Column(String(100), ForeignKey("customer.name"))

    # rating connected to the customer; unsure if I need to do the backpopulates thing here?
