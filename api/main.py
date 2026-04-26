from __future__ import annotations

from typing import Any

from fastapi import Body, FastAPI, HTTPException
from pydantic import ValidationError

from src.sentiment_monitor.inference import predict_batch
from src.sentiment_monitor.schemas import PredictionRequest, PredictionResponse


app = FastAPI(
    title="Air Paradis Sentiment Monitor API",
    description="API MVP de classification de sentiment pour tweets.",
    version="1.0.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Air Paradis Sentiment Monitor API is running"}


def _extract_texts(payload: Any) -> list[str]:
    if isinstance(payload, list):
        texts = payload
    elif isinstance(payload, dict):
        texts = PredictionRequest.model_validate(payload).texts
    else:
        raise ValueError("Le payload doit être une liste de textes ou {'texts': [...]}.")

    if not all(isinstance(text, str) for text in texts):
        raise ValueError("Tous les éléments à prédire doivent être des chaînes.")
    return texts


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: Any = Body(...)) -> PredictionResponse:
    try:
        texts = _extract_texts(payload)
        results = predict_batch(texts)
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    predictions = [int(result["class_id"]) for result in results]
    return PredictionResponse(predictions=predictions, results=results)
