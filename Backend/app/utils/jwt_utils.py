import jwt
from datetime import datetime, timedelta
from typing import Optional
from app.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class JWTUtils:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Genera un token di accesso JWT.
        :param data: Dizionario con i dati da includere nel payload del token.
        :param expires_delta: Delta di tempo per la scadenza del token. Se non specificato, viene utilizzata la configurazione di default.
        :return: Token JWT codificato.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> dict:
        """
        Decodifica e verifica un token JWT.
        :param token: Il token JWT da decodificare.
        :return: Payload decodificato del token.
        :raises jwt.ExpiredSignatureError: Se il token è scaduto.
        :raises jwt.InvalidTokenError: Se il token è invalido.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Il token è scaduto.")
        except jwt.InvalidTokenError:
            raise ValueError("Il token è invalido.")

    @staticmethod
    def is_token_valid(token: str) -> bool:
        """
        Verifica se un token JWT è valido.
        :param token: Il token JWT da verificare.
        :return: True se il token è valido, False altrimenti.
        """
        try:
            JWTUtils.decode_access_token(token)
            return True
        except ValueError:
            return False
