from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.emotional_state import EmotionalState
from app.schemas.emotional_state_schema import (
    EmotionalStateCreate,
    EmotionalStateUpdate,
    EmotionalStateResponse
)
from app.schemas.ai_match_schema import AIMatchMapSchema

def create_emotional_state(db: Session, emotional_state_data: EmotionalStateCreate) -> EmotionalStateResponse:
    """
    Crea un nuovo stato emozionale e valida il campo ai_match.
    """
    try:
        # Validazione di ai_match tramite Pydantic
        if emotional_state_data.ai_match:
            AIMatchMapSchema.parse_obj(emotional_state_data.ai_match)

        new_emotional_state = EmotionalState(
            name=emotional_state_data.name,
            description=emotional_state_data.description,
            color_code=emotional_state_data.color_code,
            intensity_levels=emotional_state_data.intensity_levels,
            ai_match=emotional_state_data.ai_match
        )
        db.add(new_emotional_state)
        db.commit()
        db.refresh(new_emotional_state)
        return EmotionalStateResponse.from_orm(new_emotional_state)

    except ValueError as ve:
        db.rollback()
        raise ValueError(f"Errore di validazione: {ve}")

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Errore durante la creazione dello stato emozionale: {e}")

def update_emotional_state(db: Session, state_id: int, update_data: EmotionalStateUpdate) -> EmotionalStateResponse:
    """
    Aggiorna uno stato emozionale esistente e valida il campo ai_match.
    """
    try:
        emotional_state = db.query(EmotionalState).filter(EmotionalState.id == state_id).first()
        if not emotional_state:
            raise ValueError(f"Stato emozionale con ID {state_id} non trovato.")

        # Validazione di ai_match tramite Pydantic
        if update_data.ai_match:
            AIMatchMapSchema.parse_obj(update_data.ai_match)

        # Aggiornamento dei campi
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(emotional_state, field, value)

        db.commit()
        db.refresh(emotional_state)
        return EmotionalStateResponse.from_orm(emotional_state)

    except ValueError as ve:
        db.rollback()
        raise ValueError(f"Errore di validazione: {ve}")

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Errore durante l'aggiornamento dello stato emozionale: {e}")

def delete_emotional_state(db: Session, state_id: int) -> bool:
    """
    Elimina uno stato emozionale esistente.
    """
    try:
        emotional_state = db.query(EmotionalState).filter(EmotionalState.id == state_id).first()
        if not emotional_state:
            raise ValueError(f"Stato emozionale con ID {state_id} non trovato.")

        db.delete(emotional_state)
        db.commit()
        return True

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Errore durante l'eliminazione dello stato emozionale: {e}")

def get_emotional_state_by_id(db: Session, state_id: int) -> EmotionalStateResponse:
    """
    Recupera uno stato emozionale per ID.
    """
    emotional_state = db.query(EmotionalState).filter(EmotionalState.id == state_id).first()
    if not emotional_state:
        raise ValueError(f"Stato emozionale con ID {state_id} non trovato.")
    return EmotionalStateResponse.from_orm(emotional_state)

def list_emotional_states(db: Session) -> list[EmotionalStateResponse]:
    """
    Recupera tutti gli stati emozionali.
    """
    emotional_states = db.query(EmotionalState).all()
    return [EmotionalStateResponse.from_orm(state) for state in emotional_states]
