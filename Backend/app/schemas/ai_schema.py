from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

# AI Engine Schemas
class AIEngineBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    api_endpoint: str = Field(...)
    pricing_model: Dict[str, float] = Field(..., description="JSON structure with cost details (e.g., {'type': 'per_call', 'cost_per_call': 0.005})")
    max_tokens: Optional[int] = None
    latency_ms: Optional[int] = Field(0, description="Average response latency in milliseconds")

class AIEngineCreate(AIEngineBase):
    pass

class AIEngineResponse(AIEngineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# AI Preset Schemas
class AIPresetBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    gender: Optional[str] = Field("neutral", description="Gender of the AI voice")
    pitch: int = Field(0, description="Voice pitch: positive for higher, negative for lower")
    speech_rate: float = Field(1.0, description="Speech rate: 1.0 is normal")
    accent: Optional[str] = None
    voice_quality: Optional[str] = Field("natural", description="Voice quality, e.g., natural or robotic")
    tone: Optional[str] = Field("neutral", description="Tone of the communication")
    formality_level: Optional[str] = Field("semi-formal", description="Formality level of responses")
    empathy_level: int = Field(2, description="Empathy level: 1 to 3")
    focus: Optional[str] = Field("supportive", description="Focus of the communication")
    language: Optional[str] = Field("en", description="Language of the AI")
    proactive_level: int = Field(1, description="Proactivity level: 1 to 3")
    response_length: Optional[str] = Field("medium", description="Response length: short, medium, or long")
    personality: Optional[str] = Field("neutral", description="Personality setting of the AI")
    color_theme: Optional[str] = Field("#000000", description="Hex color theme for responses")
    dynamic_behavior: bool = Field(True, description="Whether the AI dynamically adapts responses")
    is_premium: bool = Field(False, description="If the preset is premium-only")

class AIPresetCreate(AIPresetBase):
    pass

class AIPresetResponse(AIPresetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# AI Usage Log Schemas
class AIUsageLogBase(BaseModel):
    user_id: int
    engine_id: int
    preset_id: Optional[int] = None
    emotional_state_id: Optional[int] = None
    cost: float = Field(0.0, description="Cost of the AI request")
    latency_ms: Optional[int] = None
    status: str = Field(..., description="Status of the request, e.g., success or failure")
    error_message: Optional[str] = None

class AIUsageLogCreate(AIUsageLogBase):
    request_payload: Dict[str, str] = Field(..., description="Details of the request sent to the AI")
    response_payload: Optional[Dict[str, str]] = Field(None, description="Details of the AI response")

class AIUsageLogResponse(AIUsageLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Base class for User AI Settings
class UserAISettingsBase(BaseModel):
    ai_preset_id: int
    custom_gender: Optional[str] = None
    custom_pitch: Optional[int] = None
    custom_speech_rate: Optional[float] = None
    custom_accent: Optional[str] = None
    custom_voice_quality: Optional[str] = None
    custom_tone: Optional[str] = None
    custom_formality_level: Optional[str] = None
    custom_empathy_level: Optional[int] = None
    custom_focus: Optional[str] = None
    custom_language: Optional[str] = None
    custom_proactive_level: Optional[int] = None
    custom_response_length: Optional[str] = None
    custom_personality: Optional[str] = None
    custom_color_theme: Optional[str] = None
    custom_dynamic_behavior: Optional[bool] = None

# For creating User AI Settings
class UserAISettingsCreate(UserAISettingsBase):
    pass

# For updating User AI Settings
class UserAISettingsUpdate(BaseModel):
    ai_preset_id: Optional[int] = None
    custom_gender: Optional[str] = None
    custom_pitch: Optional[int] = None
    custom_speech_rate: Optional[float] = None
    custom_accent: Optional[str] = None
    custom_voice_quality: Optional[str] = None
    custom_tone: Optional[str] = None
    custom_formality_level: Optional[str] = None
    custom_empathy_level: Optional[int] = None
    custom_focus: Optional[str] = None
    custom_language: Optional[str] = None
    custom_proactive_level: Optional[int] = None
    custom_response_length: Optional[str] = None
    custom_personality: Optional[str] = None
    custom_color_theme: Optional[str] = None
    custom_dynamic_behavior: Optional[bool] = None

# For responses
class UserAISettingsResponse(UserAISettingsBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
