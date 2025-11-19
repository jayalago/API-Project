from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class RecipesBase(BaseModel):
    pass

class RecipesCreate(RecipesBase):
    pass

class RecipesUpdate(BaseModel):
    pass

class Recipes(RecipesBase):
    pass

    class ConfigDict:
        from_attributes = True