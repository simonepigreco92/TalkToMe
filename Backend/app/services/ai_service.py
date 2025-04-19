from sqlalchemy.orm import Session
from app.models.ai import AIEngine, AIPreset, UserAISettings
from app.schemas.ai_schema import (
    AIEngineBase,
    AIEngineCreate,
    AIPresetBase,
    AIPresetCreate,
    UserAISettingsBase,
    UserAISettingsCreate,
    UserAISettingsUpdate
)

from app.schemas.pricing_model_schema import PricingModelSchema  # Import per la validazione
from app.models.user import User
from app.db.session import get_db
from fastapi import HTTPException, status

# AIEngine Services

def get_ai_engines(db: Session):
    """Retrieve all available AI engines."""
    return db.query(AIEngine).all()

    """Create a new AI engine."""
    # Validazione di pricing_model
    try:
        PricingModelSchema.parse_obj(ai_engine_data.pricing_model)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid pricing model: {e}",
        )

    ai_engine = AIEngine(**ai_engine_data.dict())
    db.add(ai_engine)
    db.commit()
    db.refresh(ai_engine)
    return ai_engine

# AIPreset Services

def get_ai_presets(db: Session):
    """Retrieve all available AI presets."""
    return db.query(AIPreset).all()

def create_ai_preset(db: Session, ai_preset_data: AIPresetCreate):
    """Create a new AI preset."""
    ai_preset = AIPreset(**ai_preset_data.dict())
    db.add(ai_preset)
    db.commit()
    db.refresh(ai_preset)
    return ai_preset

# UserAISettings Services

def get_user_ai_settings(db: Session, user_id: int):
    """Retrieve AI settings for a specific user."""
    user_ai_settings = db.query(UserAISettings).filter(UserAISettings.user_id == user_id).first()
    if not user_ai_settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI settings for user with ID {user_id} not found."
        )
    return user_ai_settings

def create_user_ai_settings(db: Session, user_id: int, settings_data: UserAISettingsCreate):
    """Create AI settings for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )
    user_ai_settings = UserAISettings(user_id=user_id, **settings_data.dict())
    db.add(user_ai_settings)
    db.commit()
    db.refresh(user_ai_settings)
    return user_ai_settings

def update_user_ai_settings(db: Session, user_id: int, settings_data: UserAISettingsUpdate):
    """Update AI settings for a user."""
    user_ai_settings = db.query(UserAISettings).filter(UserAISettings.user_id == user_id).first()
    if not user_ai_settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI settings for user with ID {user_id} not found."
        )
    for key, value in settings_data.dict(exclude_unset=True).items():
        setattr(user_ai_settings, key, value)
    db.commit()
    db.refresh(user_ai_settings)
    return user_ai_settings

def delete_user_ai_settings(db: Session, user_id: int):
    """Delete AI settings for a user."""
    user_ai_settings = db.query(UserAISettings).filter(UserAISettings.user_id == user_id).first()
    if not user_ai_settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI settings for user with ID {user_id} not found."
        )
    db.delete(user_ai_settings)
    db.commit()
    return {"message": "AI settings deleted successfully."}
