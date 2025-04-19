from fastapi import FastAPI
from app.db.session import engine, Base
from app.routes import user_routes, room_routes, ai_routes, subscription_routes, emotional_state_routes

# Creazione del database (se non già esistente)
Base.metadata.create_all(bind=engine)

# Istanza dell'app FastAPI
app = FastAPI(
    title="TalkToMe Backend",
    description="Backend per il progetto TalkToMe",
    version="1.0.0"
)

# Inclusione delle rotte
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(room_routes.router, prefix="/rooms", tags=["Rooms"])
app.include_router(ai_routes.router, prefix="/ai", tags=["AI"])
app.include_router(subscription_routes.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(emotional_state_routes.router, prefix="/emotional-states", tags=["Emotional States"])
