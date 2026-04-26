from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "tfidf_vectorizer.pkl"
DEFAULT_TWEET_PREVIEW_CHARS = 160


@dataclass(frozen=True)
class AppConfig:
    """Configuration runtime partagée entre API, Streamlit et monitoring."""

    model_path: Path
    azure_connection_string: str
    tweet_preview_chars: int


def get_config() -> AppConfig:
    """Construit la configuration à partir des variables d'environnement."""
    preview_chars = os.getenv("TWEET_PREVIEW_CHARS", str(DEFAULT_TWEET_PREVIEW_CHARS))
    try:
        preview_chars_value = int(preview_chars)
    except ValueError:
        preview_chars_value = DEFAULT_TWEET_PREVIEW_CHARS

    return AppConfig(
        model_path=Path(os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH)),
        azure_connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", ""),
        tweet_preview_chars=max(20, preview_chars_value),
    )
