from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CustomerBase(BaseModel):
    pass

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    pass

class Customer(CustomerBase):
    pass

    class ConfigDict:
        from_attributes = True