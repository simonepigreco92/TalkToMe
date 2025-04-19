from sqlalchemy import Column, Integer, String, Boolean, JSON, Text, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base

class AIEngine(Base):
    __tablename__ = "ai_engines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    api_endpoint = Column(Text, nullable=False)
    api_key = Column(String(255), nullable=False)
    pricing_model = Column(JSON, nullable=False)  # JSON to store pricing details
    max_tokens = Column(Integer)
    latency_ms = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default="now()")
    updated_at = Column(TIMESTAMP, default="now()")

    usage_logs = relationship("AIUsageLog", back_populates="engine")

    def validate_pricing_model(self):
        try:
            PricingModelSchema.parse_obj(self.pricing_model)
        except Exception as e:
            raise ValueError(f"Errore nella validazione di pricing_model: {e}")

@event.listens_for(AIEngine, "before_insert")
@event.listens_for(AIEngine, "before_update")
def validate_ai_engine(mapper, connection, target):
    target.validate_pricing_model()

class AIPreset(Base):
    __tablename__ = "ai_presets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    gender = Column(String(50), default="neutral")
    pitch = Column(Integer, default=0)
    speech_rate = Column(DECIMAL(3, 2), default=1.0)
    accent = Column(String(50))
    voice_quality = Column(String(50), default="natural")
    tone = Column(String(50), default="neutral")
    formality_level = Column(String(50), default="semi-formal")
    empathy_level = Column(Integer, default=2)
    focus = Column(String(50), default="supportive")
    language = Column(String(10), default="en")
    proactive_level = Column(Integer, default=1)
    response_length = Column(String(50), default="medium")
    personality = Column(String(50), default="neutral")
    color_theme = Column(String(7), default="#000000")
    dynamic_behavior = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default="now()")
    updated_at = Column(TIMESTAMP, default="now()")

    user_settings = relationship("UserAISettings", back_populates="preset")

class AIUsageLog(Base):
    __tablename__ = "ai_usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    engine_id = Column(Integer, ForeignKey("ai_engines.id"), nullable=False)
    preset_id = Column(Integer, ForeignKey("ai_presets.id"))
    emotional_state_id = Column(Integer, ForeignKey("emotional_states.id"))
    request_payload = Column(JSON, nullable=False)
    response_payload = Column(JSON)
    cost = Column(DECIMAL(10, 4), default=0.0, nullable=False)
    premium_discount = Column(DECIMAL(10, 4), default=0.0)
    latency_ms = Column(Integer)
    status = Column(String(50), nullable=False)
    error_message = Column(Text)
    created_at = Column(TIMESTAMP, default="now()")

    user = relationship("User", back_populates="usage_logs")
    engine = relationship("AIEngine", back_populates="usage_logs")
    preset = relationship("AIPreset")
    emotional_state = relationship("EmotionalState")
