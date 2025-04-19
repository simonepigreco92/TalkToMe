from pydantic import BaseModel, Field
from typing import Dict

class AIMatchSchema(BaseModel):
    ai_preset: str = Field(..., description="Preset AI")
    affinity: int = Field(..., ge=0, le=100, description="Percentuale di affinità (0-100)")

class AIMatchMapSchema(BaseModel):
    __root__: Dict[str, AIMatchSchema]