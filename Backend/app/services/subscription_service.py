from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.schemas.subscription_schema import SubscriptionCreate, SubscriptionUpdate
from datetime import datetime
from typing import Optional


class SubscriptionService:
    @staticmethod
    def create_subscription(db: Session, subscription_data: SubscriptionCreate) -> Subscription:

    # Validazione del tipo di sottoscrizione
    subscription_data.subscription_type = validate_subscription_type(subscription_data.subscription_type)

        """
        Crea una nuova sottoscrizione per un utente.
        """
        new_subscription = Subscription(
            user_id=subscription_data.user_id,
            subscription_type=subscription_data.subscription_type,
            start_date=subscription_data.start_date or datetime.utcnow(),
            end_date=subscription_data.end_date,
            is_active=subscription_data.is_active,
            auto_renew=subscription_data.auto_renew,
            payment_method=subscription_data.payment_method,
        )
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        return new_subscription

    @staticmethod
    def update_subscription(
        db: Session, subscription_id: int, subscription_data: SubscriptionUpdate
    ) -> Optional[Subscription]:
        """
        Aggiorna una sottoscrizione esistente.
        """
        subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
        if not subscription:
            return None

        for key, value in subscription_data.dict(exclude_unset=True).items():
            setattr(subscription, key, value)

        subscription.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(subscription)
        return subscription

    @staticmethod
    def get_subscription_by_user_id(db: Session, user_id: int) -> Optional[Subscription]:
        """
        Recupera la sottoscrizione attiva di un utente.
        """
        return (
            db.query(Subscription)
            .filter(Subscription.user_id == user_id, Subscription.is_active == True)
            .first()
        )

    @staticmethod
    def is_user_premium(db: Session, user_id: int) -> bool:
        """
        Verifica se un utente ha una sottoscrizione premium attiva.
        """
        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.is_active == True,
                Subscription.subscription_type == "premium",
            )
            .first()
        )
        return subscription is not None

    @staticmethod
    def deactivate_subscription(db: Session, subscription_id: int) -> bool:
        """
        Disattiva una sottoscrizione esistente.
        """
        subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
        if not subscription:
            return False

        subscription.is_active = False
        subscription.updated_at = datetime.utcnow()
        db.commit()
        return True
