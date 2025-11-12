from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PromotionBase(BaseModel):
    pass

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    pass

class Promotion(PromotionBase):
    pass

    class ConfigDict:
        from_attributes = True