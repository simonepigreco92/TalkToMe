from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_type = Column(String(50), nullable=False, default="free")
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)  # Null for free subscriptions or unlimited plans
    is_active = Column(Boolean, default=True)
    payment_method = Column(String(50), nullable=True)  # Optional: e.g., "credit_card", "paypal"
    auto_renew = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="subscriptions")

# Add this relationship in the User model (user.py):
# subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
