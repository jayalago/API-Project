from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Customer(Base):
    __tablename__ = "customers"

    name = Column(String(100), primary_key=True, index=True)
    email = Column(String(100))
    phone_number = Column(String(10))
    address = Column(String(100))

