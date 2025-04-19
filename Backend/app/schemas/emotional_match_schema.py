from pydantic import BaseModel, Field, root_validator
from typing import Dict


class EmotionalMatchSchema(BaseModel):
    matches: Dict[str, int] = Field(
        ..., description="Mappa delle emozioni con le relative percentuali"
    )

    @root_validator
    def validate_percentages(cls, values):
        matches = values.get("matches", {})
        for emotion, percentage in matches.items():
            if not (0 <= percentage <= 100):
                raise ValueError(f"Il valore per {emotion} deve essere compreso tra 0 e 100.")
        return values
