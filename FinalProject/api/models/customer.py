from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    phone_number = Column(String(15), default = "Not provided.")
    address = Column(String(150))

    orders = relationship("Order", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")
    ratings = relationship("Rating", back_populates="customer")

