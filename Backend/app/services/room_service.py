from sqlalchemy.orm import Session
from app.models.room import Room, RoomCheckin, UserRoom
from app.models.user import User
from app.schemas.room_schema import (
    RoomCreate,
    RoomUpdate,
    RoomCheckinBase,
    RoomCheckinResponse,
    UserRoomCreate,
    UserRoomUpdate,
)

from app.schemas.emotional_match_schema import EmotionalMatchSchema  # Import per la validazione
from app.utils.randomizer import weighted_random_choice
from datetime import date
from fastapi import HTTPException, status

def create_room(db: Session, room_data: RoomCreate) -> Room:
    """Create a new room."""
    # Validazione di emotional_match
    try:
        EmotionalMatchSchema.parse_obj(room_data.emotional_match)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid emotional match structure: {e}",
        )

    new_room = Room(**room_data.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

def update_room(db: Session, room_id: int, room_data: RoomUpdate) -> Room:
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    for key, value in room_data.dict(exclude_unset=True).items():
        setattr(room, key, value)
    db.commit()
    db.refresh(room)
    return room

def delete_room(db: Session, room_id: int) -> None:
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    db.delete(room)
    db.commit()

def create_room_checkin(db: Session, user_id: int, room_id: int, is_random: bool) -> RoomCheckin:
    room_checkin = db.query(RoomCheckin).filter(
        RoomCheckin.user_id == user_id,
        RoomCheckin.room_id == room_id
    ).first()

    if room_checkin:
        room_checkin.checkin_count += 1
        room_checkin.last_checkin = date.today()
    else:
        room_checkin = RoomCheckin(
            user_id=user_id,
            room_id=room_id,
            is_random=is_random,
            checkin_count=1,
            last_checkin=date.today()
        )
        db.add(room_checkin)

    db.commit()
    db.refresh(room_checkin)
    return room_checkin

def update_room_customization(db: Session, user_id: int, customization_data: UserRoomUpdate) -> UserRoom:
    user_room = db.query(UserRoom).filter(
        UserRoom.user_id == user_id,
        UserRoom.room_id == customization_data.room_id
    ).first()

    if not user_room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserRoom not found"
        )

    for key, value in customization_data.dict(exclude_unset=True).items():
        setattr(user_room, key, value)

    db.commit()
    db.refresh(user_room)
    return user_room

def create_user_room(db: Session, user_id: int, user_room_data: UserRoomCreate) -> UserRoom:
    user_room = UserRoom(
        user_id=user_id,
        **user_room_data.dict()
    )
    db.add(user_room)
    db.commit()
    db.refresh(user_room)
    return user_room

def update_user_room(db: Session, user_id: int, user_room_data: UserRoomUpdate) -> UserRoom:
    user_room = db.query(UserRoom).filter(
        UserRoom.user_id == user_id,
        UserRoom.room_id == user_room_data.room_id
    ).first()

    if not user_room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserRoom not found"
        )

    for key, value in user_room_data.dict(exclude_unset=True).items():
        setattr(user_room, key, value)

    db.commit()
    db.refresh(user_room)
    return user_room

def delete_user_room(db: Session, user_id: int, room_id: int) -> None:
    user_room = db.query(UserRoom).filter(
        UserRoom.user_id == user_id,
        UserRoom.room_id == room_id
    ).first()

    if not user_room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserRoom not found"
        )

    db.delete(user_room)
    db.commit()
