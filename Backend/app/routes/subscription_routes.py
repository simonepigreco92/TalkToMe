from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.subscription_schema import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from app.services.subscription_service import SubscriptionService

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"]
)


@router.post("/", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_subscription(subscription_data: SubscriptionCreate, db: Session = Depends(get_db)):
    """
    Endpoint per creare una nuova sottoscrizione.
    """
    try:
        return SubscriptionService.create_subscription(db, subscription_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=SubscriptionResponse)
def get_subscription(user_id: int, db: Session = Depends(get_db)):
    """
    Endpoint per recuperare una sottoscrizione attiva per un utente.
    """
    subscription = SubscriptionService.get_subscription_by_user_id(db, user_id)
    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found.")
    return subscription


@router.put("/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(
    subscription_id: int, subscription_data: SubscriptionUpdate, db: Session = Depends(get_db)
):
    """
    Endpoint per aggiornare una sottoscrizione esistente.
    """
    updated_subscription = SubscriptionService.update_subscription(db, subscription_id, subscription_data)
    if not updated_subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found.")
    return updated_subscription


@router.post("/{subscription_id}/deactivate", status_code=status.HTTP_200_OK)
def deactivate_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """
    Endpoint per disattivare una sottoscrizione esistente.
    """
    success = SubscriptionService.deactivate_subscription(db, subscription_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found.")
    return {"message": "Subscription deactivated successfully"}
