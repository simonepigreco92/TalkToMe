from pydantic import BaseModel, Field, validator
from typing import Literal, Optional


class PricingModelSchema(BaseModel):
    type: Literal["per_call", "subscription", "free"] = Field(
        ..., description="Tipo di modello di pricing (per_call, subscription, free)"
    )
    cost_per_call: Optional[float] = Field(
        None, description="Costo per chiamata in caso di modello per_call", ge=0
    )
    premium_discount: Optional[float] = Field(
        None, description="Percentuale di sconto per utenti premium", ge=0, le=100
    )

    @validator("cost_per_call", always=True)
    def validate_cost_per_call(cls, value, values):
        if values["type"] == "per_call" and value is None:
            raise ValueError("cost_per_call è obbligatorio per il modello per_call.")
        return value

    @validator("premium_discount", always=True)
    def validate_premium_discount(cls, value, values):
        if values["type"] == "free" and value is not None:
            raise ValueError("premium_discount non è applicabile per il modello free.")
        return value
