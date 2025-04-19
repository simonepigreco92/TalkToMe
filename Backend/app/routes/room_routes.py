from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.room_schema import (
    RoomCreate,
    RoomUpdate,
    RoomCheckinBase,
    RoomCheckinResponse,
    UserRoomCreate,
    UserRoomUpdate,
)
from app.services.room_service import (
    create_room,
    update_room,
    delete_room,
    create_room_checkin,
    update_room_customization,
    create_user_room,
    update_user_room,
    delete_user_room,
)
from typing import List

router = APIRouter()

# Room routes
@router.post("/", response_model=RoomCreate, status_code=status.HTTP_201_CREATED)
def create_room_route(room_data: RoomCreate, db: Session = Depends(get_db)):
    return create_room(db, room_data)


@router.put("/{room_id}", response_model=RoomUpdate)
def update_room_route(room_id: int, room_data: RoomUpdate, db: Session = Depends(get_db)):
    return update_room(db, room_id, room_data)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_route(room_id: int, db: Session = Depends(get_db)):
    delete_room(db, room_id)


# Room Checkin routes
@router.post("/{room_id}/checkin", response_model=RoomCheckinResponse)
def create_room_checkin_route(
    room_id: int, checkin_data: RoomCheckinBase, db: Session = Depends(get_db)
):
    return create_room_checkin(
        db, checkin_data.user_id, room_id, checkin_data.is_random
    )


# User Room routes
@router.post("/user-room/", response_model=UserRoomCreate, status_code=status.HTTP_201_CREATED)
def create_user_room_route(user_room_data: UserRoomCreate, db: Session = Depends(get_db)):
    return create_user_room(db, user_room_data.user_id, user_room_data)


@router.put("/user-room/", response_model=UserRoomUpdate)
def update_user_room_route(user_room_data: UserRoomUpdate, db: Session = Depends(get_db)):
    return update_user_room(db, user_room_data.user_id, user_room_data)


@router.delete("/user-room/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_room_route(user_id: int, room_id: int, db: Session = Depends(get_db)):
    delete_user_room(db, user_id, room_id)
