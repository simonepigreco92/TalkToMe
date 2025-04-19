from typing import Dict, Any
import random

def weighted_random_choice(weights: Dict[Any, float]) -> Any:
    """
    Seleziona un elemento casualmente in base ai pesi forniti.

    :param weights: Dizionario con elementi e i loro pesi associati.
    :return: L'elemento selezionato.
    """
    if not weights:
        raise ValueError("Il dizionario dei pesi non può essere vuoto.")

    if not all(weight >= 0 for weight in weights.values()):
        raise ValueError("I pesi devono essere valori non negativi.")

    total_weight = sum(weights.values())
    if total_weight == 0:
        raise ValueError("La somma dei pesi deve essere maggiore di zero.")

    cumulative_weights = []
    current_weight = 0
    for weight in weights.values():
        current_weight += weight
        cumulative_weights.append(current_weight)

    random_value = random.uniform(0, cumulative_weights[-1])
    for index, cumulative_weight in enumerate(cumulative_weights):
        if random_value <= cumulative_weight:
            return list(weights.keys())[index]
