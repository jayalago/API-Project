from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class MenuBase(BaseModel):
    pass

class MenuCreate(MenuBase):
    pass

class MenuUpdate(BaseModel):
    pass

class Menu(MenuBase):
    pass

    class ConfigDict:
        from_attributes = True