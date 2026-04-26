from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from src.sentiment_monitor.config import get_config


def sentiment_label(class_id: int) -> str:
    """Mappe la classe numérique vers un label lisible."""
    return "Positif" if int(class_id) == 1 else "Négatif"


@lru_cache(maxsize=1)
def load_model(model_path: str | Path | None = None) -> Any:
    """Charge le pipeline scikit-learn une seule fois par processus."""
    path = Path(model_path) if model_path is not None else get_config().model_path
    return joblib.load(path)


def predict_sentiment(text: str, model: Any | None = None) -> dict[str, object]:
    """Prédit le sentiment d'un texte sans modifier le pipeline métier."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Le texte à prédire ne peut pas être vide.")

    active_model = model if model is not None else load_model()
    class_id = int(active_model.predict([text])[0])
    probability = None

    if hasattr(active_model, "predict_proba"):
        probabilities = np.asarray(active_model.predict_proba([text])[0], dtype=float)
        probability = float(probabilities.max())

    return {
        "class_id": class_id,
        "label": sentiment_label(class_id),
        "probability": probability,
    }


def predict_batch(texts: list[str], model: Any | None = None) -> list[dict[str, object]]:
    """Prédit une liste de textes et ajoute l'index source."""
    if not texts:
        raise ValueError("La liste de textes ne peut pas être vide.")

    active_model = model if model is not None else load_model()
    results = []
    for index, text in enumerate(texts):
        result = predict_sentiment(text, model=active_model)
        results.append({"text_index": index, **result})
    return results
