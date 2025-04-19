from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Base schema
class SubscriptionBase(BaseModel):
    subscription_type: str = Field(..., max_length=50)  # Tipo di sottoscrizione (es. premium, trial)
    start_date: Optional[datetime]  # Data di inizio abbonamento
    end_date: Optional[datetime]  # Data di fine abbonamento (opzionale per abbonamenti senza scadenza)
    is_active: bool = True  # Stato attivo/inattivo
    auto_renew: Optional[bool] = False  # Se l'abbonamento si rinnova automaticamente
    payment_method: Optional[str] = Field(None, max_length=50)  # Metodo di pagamento (opzionale)


# Create schema
class SubscriptionCreate(SubscriptionBase):
    user_id: int = Field(..., description="L'ID dell'utente associato alla sottoscrizione")  # FK all'utente


# Update schema
class SubscriptionUpdate(BaseModel):
    subscription_type: Optional[str] = Field(None, max_length=50)  # Tipo di sottoscrizione
    end_date: Optional[datetime]  # Aggiornamento data di fine
    is_active: Optional[bool]  # Modifica stato attivo/inattivo
    auto_renew: Optional[bool]  # Aggiornamento del rinnovo automatico
    payment_method: Optional[str] = Field(None, max_length=50)  # Metodo di pagamento


# Response schema
class SubscriptionResponse(SubscriptionBase):
    id: int = Field(..., description="ID univoco della sottoscrizione")  # PK della sottoscrizione
    user_id: int = Field(..., description="ID dell'utente associato")  # FK all'utente
    created_at: datetime = Field(..., description="Data di creazione della sottoscrizione")
    updated_at: datetime = Field(..., description="Ultima modifica della sottoscrizione")

    class Config:
        orm_mode = True  # Permette la compatibilità con SQLAlchemy
