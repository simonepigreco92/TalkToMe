import os
from dotenv import load_dotenv

# Caricamento delle variabili d'ambiente dal file .env
load_dotenv()

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./talktome.db")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# App settings
APP_NAME = os.getenv("APP_NAME", "TalkToMe")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Email settings (opzionale, in caso di integrazione con sistemi di notifica)
EMAIL_SERVER = os.getenv("EMAIL_SERVER", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"

# Altre variabili di configurazione possono essere aggiunte qui
