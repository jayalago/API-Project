from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class RecipesBase(BaseModel):
    amount: int

class RecipesCreate(RecipesBase):
    sandwich_id: int
    resources_id: int

class RecipesUpdate(BaseModel):
    sandwich_id: Optional[int] = None
    resources_id: Optional[int] = None
    amount: Optional[int] = None

class Recipes(RecipesBase):
    pass

    class ConfigDict:
        from_attributes = True