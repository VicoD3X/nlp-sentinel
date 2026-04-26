from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "tfidf_vectorizer.pkl"
DEFAULT_TWEET_PREVIEW_CHARS = 160
DEFAULT_MONITORING_BACKEND = "local"
DEFAULT_LOCAL_MONITORING_PATH = PROJECT_ROOT / "logs" / "monitoring_events.jsonl"
SUPPORTED_MONITORING_BACKENDS = {"local", "azure", "both", "none"}


@dataclass(frozen=True)
class AppConfig:
    """Configuration runtime partagée entre API, Streamlit et monitoring."""

    model_path: Path = DEFAULT_MODEL_PATH
    azure_connection_string: str = ""
    tweet_preview_chars: int = DEFAULT_TWEET_PREVIEW_CHARS
    monitoring_backend: str = DEFAULT_MONITORING_BACKEND
    local_monitoring_path: Path = DEFAULT_LOCAL_MONITORING_PATH


def _project_path_from_env(value: str | None, default_path: Path) -> Path:
    """Convertit un chemin d'environnement en chemin projet portable."""
    if not value:
        return default_path
    path = Path(value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def _normalize_monitoring_backend(value: str | None) -> str:
    """Normalise le backend de monitoring demandé."""
    backend = (value or DEFAULT_MONITORING_BACKEND).strip().lower()
    if backend not in SUPPORTED_MONITORING_BACKENDS:
        return DEFAULT_MONITORING_BACKEND
    return backend


def get_config() -> AppConfig:
    """Construit la configuration à partir des variables d'environnement."""
    preview_chars = os.getenv("TWEET_PREVIEW_CHARS", str(DEFAULT_TWEET_PREVIEW_CHARS))
    try:
        preview_chars_value = int(preview_chars)
    except ValueError:
        preview_chars_value = DEFAULT_TWEET_PREVIEW_CHARS

    return AppConfig(
        model_path=_project_path_from_env(os.getenv("MODEL_PATH"), DEFAULT_MODEL_PATH),
        azure_connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", ""),
        tweet_preview_chars=max(20, preview_chars_value),
        monitoring_backend=_normalize_monitoring_backend(
            os.getenv("MONITORING_BACKEND"),
        ),
        local_monitoring_path=_project_path_from_env(
            os.getenv("LOCAL_MONITORING_PATH"),
            DEFAULT_LOCAL_MONITORING_PATH,
        ),
    )
