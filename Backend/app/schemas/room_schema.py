from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class RoomBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    base_layer_url: str = Field(...)
    is_premium: bool = Field(default=False)

class RoomCreate(RoomBase):
    overlay_layers: Optional[List[str]] = Field(None, description="Lista di layer extra opzionali per la stanza")
    emotional_match: Optional[dict] = Field(None, description="Percentuali di affinità con stati emozionali")

class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    base_layer_url: Optional[str] = None
    is_premium: Optional[bool] = None
    overlay_layers: Optional[List[str]] = None
    emotional_match: Optional[dict] = None

class RoomResponse(RoomBase):
    id: int
    overlay_layers: Optional[List[str]]
    emotional_match: Optional[dict]
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

class RoomCustomizationBase(BaseModel):
    customization: dict = Field(..., description="Dati di personalizzazione specifici dell'utente per la stanza")

class UserRoomCreate(RoomCustomizationBase):
    room_id: int = Field(..., description="ID della stanza personalizzata")

class UserRoomResponse(RoomCustomizationBase):
    id: int
    user_id: int = Field(..., description="ID dell'utente che ha personalizzato la stanza")
    room_id: int = Field(..., description="ID della stanza personalizzata")
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

# Base schema for Room Check-ins
class RoomCheckinBase(BaseModel):
    user_id: int = Field(..., description="ID dell'utente che effettua il check-in")
    room_id: int = Field(..., description="ID della stanza in cui si effettua il check-in")
    checkin_count: int = Field(1, description="Numero totale di check-in in questa stanza")
    last_checkin: Optional[datetime] = None  # Data e ora dell'ultimo check-in
    is_random: bool = Field(True, description="Indica se la stanza è stata scelta casualmente")

# Schema for creating a new Room Check-in
class RoomCheckinCreate(RoomCheckinBase):
    pass  # Inherits all fields from RoomCheckinBase

# Schema for updating a Room Check-in (e.g., incrementing the counter)
class RoomCheckinUpdate(BaseModel):
    checkin_count: int = Field(..., gt=0, description="Nuovo numero totale di check-in")
    is_random: Optional[bool] = Field(None, description="Indica se la stanza è stata scelta casualmente")

# Response schema for Room Check-ins
class RoomCheckinResponse(RoomCheckinBase):
    id: int = Field(..., description="ID univoco del check-in")
    created_at: datetime = Field(..., description="Data e ora di creazione del check-in")
    updated_at: datetime = Field(..., description="Ultima data e ora di modifica del check-in")

    class Config:
        orm_mode = True
