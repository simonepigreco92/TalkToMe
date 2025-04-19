from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100))
    avatar_url = Column(Text)
    last_login = Column(DateTime)
    language = Column(String(10), default="en")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default="CURRENT_TIMESTAMP")
    updated_at = Column(DateTime, default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    # Relationships
    user_ai_settings = relationship("UserAISettings", back_populates="user", cascade="all, delete")
    user_rooms = relationship("UserRoom", back_populates="user", cascade="all, delete")
    user_settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete")


class UserAISettings(Base):
    __tablename__ = "user_ai_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ai_preset_id = Column(Integer, ForeignKey("ai_presets.id", ondelete="CASCADE"), nullable=False)
    custom_gender = Column(String(50))
    custom_pitch = Column(Integer)
    custom_speech_rate = Column(Integer)
    custom_accent = Column(String(50))
    custom_voice_quality = Column(String(50))
    custom_tone = Column(String(50))
    custom_formality_level = Column(String(50))
    custom_empathy_level = Column(Integer)
    custom_focus = Column(String(50))
    custom_language = Column(String(10))
    custom_proactive_level = Column(Integer)
    custom_response_length = Column(String(50))
    custom_personality = Column(String(50))
    custom_color_theme = Column(String(7))
    custom_dynamic_behavior = Column(Boolean)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default="CURRENT_TIMESTAMP")
    updated_at = Column(DateTime, default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    # Relationships
    user = relationship("User", back_populates="user_ai_settings")


class UserRooms(Base):
    __tablename__ = "users_rooms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    customization = Column(Text)

    # Relationships
    user = relationship("User", back_populates="user_rooms")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(10), default="en")
    notifications_enabled = Column(Boolean, default=True)
    show_emotion_checkins = Column(Boolean, default=True)
    dark_mode_enabled = Column(Boolean, default=False)
    preferred_ai_voice = Column(String(50))
    preferred_ai_tone = Column(String(50))
    sound_notifications_enabled = Column(Boolean, default=True)
    default_room_id = Column(Integer, ForeignKey("rooms.id", ondelete="SET NULL"))
    receive_checkin_reminder = Column(Boolean, default=True)
    created_at = Column(DateTime, default="CURRENT_TIMESTAMP")
    updated_at = Column(DateTime, default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    # Relationships
    user = relationship("User", back_populates="user_settings")
