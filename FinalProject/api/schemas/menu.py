from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class MenuBase(BaseModel):
    sandwich_id: int
    resource_id: int
    price: float

class MenuCreate(MenuBase):
    sandwich_id: Optional[int] = None
    resource_id: Optional[int] = None
    price: Optional[float] = None

class MenuUpdate(BaseModel):
    pass

class Menu(MenuBase):
    id: int

    class ConfigDict:
        from_attributes = True