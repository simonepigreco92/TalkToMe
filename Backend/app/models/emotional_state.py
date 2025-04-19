from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.db.base import Base
from schemas.ai_match_schema import AIMatchMapSchema

class EmotionalState(Base):
    __tablename__ = "emotional_states"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    color_code = Column(String(7), nullable=False)  # HEX color code
    intensity_levels = Column(JSON, nullable=True)  # JSON for intensity details
    ai_match = Column(JSON, nullable=False)  # JSON for AI preset match percentages

    # Relationship to EmotionalStateCheckin
    checkins = relationship("EmotionalStateCheckin", back_populates="emotional_state")

    def validate_ai_match(self):
        """
        Convalida il campo ai_match utilizzando lo schema Pydantic.
        """
        try:
            AIMatchMapSchema.parse_obj(self.ai_match)
        except Exception as e:
            raise ValueError(f"Errore nella validazione di ai_match: {e}")

    def __repr__(self):
        return f"<EmotionalState(name={self.name}, color_code={self.color_code})>"

# Ascoltatore per la validazione
from sqlalchemy import event

@event.listens_for(EmotionalState, "before_insert")
@event.listens_for(EmotionalState, "before_update")
def validate_emotional_state(mapper, connection, target):
    """
    Trigger di validazione per EmotionalState.
    """
    target.validate_ai_match()


class EmotionalStateCheckin(Base):
    __tablename__ = "emotional_states_checkin"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    emotional_state_id = Column(Integer, ForeignKey("emotional_states.id"), nullable=False)
    intensity_level = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="emotional_state_checkins")
    emotional_state = relationship("EmotionalState", back_populates="checkins")

    def __repr__(self):
        return f"<EmotionalStateCheckin(user_id={self.user_id}, emotional_state_id={self.emotional_state_id}, intensity_level={self.intensity_level})>"
