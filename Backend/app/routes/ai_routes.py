from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.ai_schema import (
    AIEngineCreate,
    AIPresetCreate,
    UserAISettingsCreate,
    UserAISettingsUpdate,
)
from app.services.ai_service import (
    get_ai_engines,
    create_ai_engine,
    get_ai_presets,
    create_ai_preset,
    get_user_ai_settings,
    create_user_ai_settings,
    update_user_ai_settings,
    delete_user_ai_settings,
)

router = APIRouter(prefix="/ai", tags=["AI"])

# Routes for AI Engines
@router.get("/engines", response_model=list)
def list_ai_engines(db: Session = Depends(get_db)):
    """Retrieve all available AI engines."""
    return get_ai_engines(db)

@router.post("/engines", response_model=dict)
def create_ai_engine_route(ai_engine_data: AIEngineCreate, db: Session = Depends(get_db)):
    """Create a new AI engine."""
    return create_ai_engine(db, ai_engine_data)

# Routes for AI Presets
@router.get("/presets", response_model=list)
def list_ai_presets(db: Session = Depends(get_db)):
    """Retrieve all available AI presets."""
    return get_ai_presets(db)

@router.post("/presets", response_model=dict)
def create_ai_preset_route(ai_preset_data: AIPresetCreate, db: Session = Depends(get_db)):
    """Create a new AI preset."""
    return create_ai_preset(db, ai_preset_data)

# Routes for User AI Settings
@router.get("/users/{user_id}/settings", response_model=dict)
def retrieve_user_ai_settings(user_id: int, db: Session = Depends(get_db)):
    """Retrieve AI settings for a specific user."""
    return get_user_ai_settings(db, user_id)

@router.post("/users/{user_id}/settings", response_model=dict)
def create_user_ai_settings_route(
    user_id: int, settings_data: UserAISettingsCreate, db: Session = Depends(get_db)
):
    """Create AI settings for a user."""
    return create_user_ai_settings(db, user_id, settings_data)

@router.put("/users/{user_id}/settings", response_model=dict)
def update_user_ai_settings_route(
    user_id: int, settings_data: UserAISettingsUpdate, db: Session = Depends(get_db)
):
    """Update AI settings for a user."""
    return update_user_ai_settings(db, user_id, settings_data)

@router.delete("/users/{user_id}/settings", response_model=dict)
def delete_user_ai_settings_route(user_id: int, db: Session = Depends(get_db)):
    """Delete AI settings for a user."""
    return delete_user_ai_settings(db, user_id)
