from pydantic import BaseModel, Field
from typing import Optional

# Base User schema
class UserBase(BaseModel):
    display_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = None
    language: Optional[str] = "en"
    is_active: Optional[bool] = True

# User creation schema
class UserCreate(UserBase):
    email: str = Field(..., max_length=255)
    password_hash: str = Field(..., min_length=8, max_length=128)

# User update schema
class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = None
    language: Optional[str] = "en"
    is_active: Optional[bool] = True

# User response schema
class UserResponse(UserBase):
    id: int
    email: str
    class Config:
        orm_mode = True

# User delete schema
class UserDelete(BaseModel):
    id: int

# User settings creation schema
class UserSettingsCreate(BaseModel):
    language: Optional[str] = "en"
    notifications_enabled: Optional[bool] = True
    show_emotion_checkins: Optional[bool] = True
    dark_mode_enabled: Optional[bool] = False
    preferred_ai_voice: Optional[str] = None
    preferred_ai_tone: Optional[str] = None
    sound_notifications_enabled: Optional[bool] = True
    default_room_id: Optional[int] = None
    receive_checkin_reminder: Optional[bool] = True

# User settings update schema
class UserSettingsUpdate(BaseModel):
    language: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    show_emotion_checkins: Optional[bool] = None
    dark_mode_enabled: Optional[bool] = None
    preferred_ai_voice: Optional[str] = None
    preferred_ai_tone: Optional[str] = None
    sound_notifications_enabled: Optional[bool] = None
    default_room_id: Optional[int] = None
    receive_checkin_reminder: Optional[bool] = None

# User settings output schema
class UserSettingsOut(BaseModel):
    id: int
    user_id: int
    language: Optional[str]
    notifications_enabled: Optional[bool]
    show_emotion_checkins: Optional[bool]
    dark_mode_enabled: Optional[bool]
    preferred_ai_voice: Optional[str]
    preferred_ai_tone: Optional[str]
    sound_notifications_enabled: Optional[bool]
    default_room_id: Optional[int]
    receive_checkin_reminder: Optional[bool]
    class Config:
        orm_mode = True
