from __future__ import annotations

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Payload officiel de prédiction."""

    texts: list[str] = Field(..., min_length=1)


class PredictionResult(BaseModel):
    """Résultat détaillé pour un texte."""

    text_index: int
    class_id: int
    label: str
    probability: float | None = None


class PredictionResponse(BaseModel):
    """Réponse API compatible avec l'ancien format `predictions`."""

    predictions: list[int]
    results: list[PredictionResult]
