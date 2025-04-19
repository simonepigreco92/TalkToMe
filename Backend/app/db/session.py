from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import DATABASE_URL

# Configurazione del motore di database
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica dello stato della connessione prima di utilizzarla
)

# Creazione della session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funzione per ottenere una sessione del database
def get_db():
    """
    Generator che fornisce una sessione del database.
    Assicura la chiusura della sessione dopo l'utilizzo.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
