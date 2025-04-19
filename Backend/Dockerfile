# Usa un'immagine base leggera con Python
FROM python:3.10-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file requirements per installare le dipendenze
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice nel container
COPY . .

# Esponi la porta su cui il backend sarà in ascolto
EXPOSE ${PORT:-8000}

# Comando per avviare l'app con Uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}"]
