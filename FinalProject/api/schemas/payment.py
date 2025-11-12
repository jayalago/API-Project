from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PaymentBase(BaseModel):
    pass

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    pass

class Payment(PaymentBase):
    pass

    class ConfigDict:
        from_attributes = True