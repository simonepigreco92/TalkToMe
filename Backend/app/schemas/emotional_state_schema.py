from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date, datetime

# EmotionalState Schemas
class EmotionalStateBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = None
    color_code: str = Field(..., regex=r"^#[0-9A-Fa-f]{6}$")
    intensity_levels: Optional[Dict[str, int]] = None  # Es: {"low": 1, "medium": 2, "high": 3}
    ai_match: Optional[Dict[str, float]] = None  # Es: {"empathetic": 0.8, "motivational": 0.5}

class EmotionalStateCreate(EmotionalStateBase):
    pass

class EmotionalStateUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    color_code: Optional[str] = Field(None, regex=r"^#[0-9A-Fa-f]{6}$")
    intensity_levels: Optional[Dict[str, int]] = None
    ai_match: Optional[Dict[str, float]] = None

class EmotionalStateResponse(EmotionalStateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# EmotionalStateCheckin Schemas
class EmotionalStateCheckinBase(BaseModel):
    intensity_level: int = Field(..., ge=1, le=10)
    notes: Optional[str] = None

class EmotionalStateCheckinCreate(EmotionalStateCheckinBase):
    emotional_state_id: int

class EmotionalStateCheckinResponse(EmotionalStateCheckinBase):
    id: int
    user_id: int
    emotional_state_id: int
    created_at: datetime

    class Config:
        orm_mode = True
