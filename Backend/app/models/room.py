from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, JSON, Date, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    base_layer_url = Column(Text, nullable=False)
    overlay_layers = Column(JSON, nullable=True)  # Dettagli per livelli extra (opzionali)
    is_premium = Column(Boolean, default=False)
    emotional_match = Column(JSON, nullable=True)  # Percentuali di affinità con stati emozionali
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relazione inversa con RoomCheckin
    checkins = relationship("RoomCheckin", back_populates="room")

    def validate_emotional_match(self):
        try:
            EmotionalMatchSchema(matches=self.emotional_match)
        except Exception as e:
            raise ValueError(f"Errore nella validazione di emotional_match: {e}")

@event.listens_for(Room, "before_insert")
@event.listens_for(Room, "before_update")
def validate_room(mapper, connection, target):
    target.validate_emotional_match()

class RoomCheckin(Base):
    __tablename__ = "rooms_checkin"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    checkin_count = Column(Integer, default=0)  # Contatore dei check-in per questa stanza
    last_checkin = Column(TIMESTAMP, nullable=True)  # Data e ora dell'ultimo check-in
    is_random = Column(Boolean, default=True)  # Indica se la stanza è stata assegnata casualmente
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relazioni
    room = relationship("Room", back_populates="checkins")
    user = relationship("User", back_populates="room_checkins")
