from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserSettingsCreate,
    UserSettingsUpdate,
    UserSettingsResponse,
)
from app.services.user_service import (
    create_user,
    get_user_by_id,
    update_user,
    delete_user,
    create_user_settings,
    get_user_settings,
    update_user_settings,
    delete_user_settings,
    UserService,
)

router = APIRouter()

# Route: Create a new user
@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_data)


# Route: Get user by ID
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)


# Route: Update a user
@router.put("/users/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user_updates: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user_updates)


# Route: Delete a user
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    delete_user(db, user_id)
    return {"detail": "User deleted successfully"}


# Route: Create user settings
@router.post("/users/{user_id}/settings/", response_model=UserSettingsResponse)
def create_settings_for_user(user_id: int, settings_data: UserSettingsCreate, db: Session = Depends(get_db)):
    return create_user_settings(db, user_id, settings_data)


# Route: Get user settings
@router.get("/users/{user_id}/settings/", response_model=UserSettingsResponse)
def get_settings_for_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_settings(db, user_id)


# Route: Update user settings
@router.put("/users/{user_id}/settings/", response_model=UserSettingsResponse)
def update_settings_for_user(user_id: int, settings_updates: UserSettingsUpdate, db: Session = Depends(get_db)):
    return update_user_settings(db, user_id, settings_updates)


# Route: Delete user settings
@router.delete("/users/{user_id}/settings/", status_code=status.HTTP_204_NO_CONTENT)
def delete_settings_for_user(user_id: int, db: Session = Depends(get_db)):
    delete_user_settings(db, user_id)
    return {"detail": "User settings deleted successfully"}


# Route: User login
@router.post("/login/")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    try:
        token = UserService.login_user(db, email, password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


# Route: Verify token
@router.post("/verify-token/")
def verify_token(token: str):
    try:
        payload = UserService.verify_token(token)
        return {"detail": "Token is valid", "payload": payload}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
