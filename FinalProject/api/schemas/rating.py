from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class RatingBase(BaseModel):
    pass

class RatingCreate(RatingBase):
    pass

class RatingUpdate(BaseModel):
    pass

class Rating(RatingBase):
    pass

    class ConfigDict:
        from_attributes = True