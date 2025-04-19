from sqlalchemy.ext.declarative import declarative_base

# Base dichiarativa per i modelli
Base = declarative_base()

# Importa qui tutti i modelli per il rilevamento da parte degli strumenti di migrazione
from app.models.user import User, UserSettings, UserRooms, UserAiSettings
from app.models.emotional_state import EmotionalState, EmotionalStateCheckin
from app.models.room import Room, RoomCheckin
from app.models.ai import AIPreset, AIEngine, AIUsageLog
from app.models.subscription import Subscription
