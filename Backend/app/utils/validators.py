import re
from fastapi import HTTPException, status

def validate_email(email: str) -> None:
    """
    Verifica se l'email è valida.
    :param email: L'indirizzo email da validare.
    :raises HTTPException: Se l'email non è valida.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Indirizzo email non valido."
        )

def validate_subscription_type(subscription_type: str) -> str:
    """
    Valida il campo subscription_type assicurandosi che rientri nei valori accettabili.

    Args:
        subscription_type (str): Il tipo di sottoscrizione da validare.

    Returns:
        str: Il valore validato.

    Raises:
        ValueError: Se il valore non è valido.
    """
    valid_types = {"free", "premium", "trial"}  # Set dei valori accettabili
    if subscription_type not in valid_types:
        raise ValueError(f"Invalid subscription_type: {subscription_type}. Must be one of {valid_types}")
    return subscription_type

