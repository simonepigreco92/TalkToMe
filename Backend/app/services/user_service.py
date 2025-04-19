from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, UserSettings
from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserSettingsCreate,
    UserSettingsUpdate,
    UserSettingsResponse
)
from app.utils.hashing import Hash
from app.utils.jwt_utils import generate_jwt_token, decode_jwt_token

# CRUD Operations for Users
def create_user(db: Session, user_data: UserCreate) -> UserResponse:
    # Check if the email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Validazione dell'email
    validate_email(user_data.email)

    hashed_password = Hash.bcrypt(user_data.password_hash)

    # Create the user
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        display_name=user_data.display_name or user_data.email.split('@')[0],
        avatar_url=user_data.avatar_url,
        language=user_data.language,
        is_active=user_data.is_active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse.from_orm(new_user)

def get_user_by_id(db: Session, user_id: int) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserResponse.from_orm(user)

def update_user(db: Session, user_id: int, updates: UserUpdate) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return UserResponse.from_orm(user)

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    db.delete(user)
    db.commit()

# CRUD Operations for UserSettings
def create_user_settings(db: Session, user_id: int, settings_data: UserSettingsCreate) -> UserSettingsResponse:
    # Check if settings already exist for the user
    existing_settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    if existing_settings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Settings already exist for this user",
        )

    # Create the settings
    new_settings = UserSettings(
        user_id=user_id,
        language=settings_data.language,
        notifications_enabled=settings_data.notifications_enabled,
        show_emotion_checkins=settings_data.show_emotion_checkins,
        dark_mode_enabled=settings_data.dark_mode_enabled,
        preferred_ai_voice=settings_data.preferred_ai_voice,
        preferred_ai_tone=settings_data.preferred_ai_tone,
        sound_notifications_enabled=settings_data.sound_notifications_enabled,
        default_room_id=settings_data.default_room_id,
        receive_checkin_reminder=settings_data.receive_checkin_reminder,
    )
    db.add(new_settings)
    db.commit()
    db.refresh(new_settings)

    return UserSettingsResponse.from_orm(new_settings)

def get_user_settings(db: Session, user_id: int) -> UserSettingsResponse:
    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User settings not found",
        )
    return UserSettingsResponse.from_orm(settings)

def update_user_settings(db: Session, user_id: int, updates: UserSettingsUpdate) -> UserSettingsResponse:
    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User settings not found",
        )

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(settings, key, value)

    db.commit()
    db.refresh(settings)

    return UserSettingsResponse.from_orm(settings)

def delete_user_settings(db: Session, user_id: int):
    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User settings not found",
        )
    db.delete(settings)
    db.commit()

class UserService:
    @staticmethod
    def login_user(db: Session, email: str, password: str) -> str:
        """
        Autentica un utente e genera un token JWT.
        """
        user = db.query(User).filter(User.email == email).first()
        if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            raise ValueError("Email o password non corretti.")

        # Genera il token JWT
        token_payload = {"user_id": user.id, "email": user.email}
        token = generate_jwt_token(token_payload)
        return token

    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verifica e decodifica un token JWT.
        """
        try:
            payload = decode_jwt_token(token)
            return payload
        except Exception as e:
            raise ValueError(f"Token non valido: {e}")
