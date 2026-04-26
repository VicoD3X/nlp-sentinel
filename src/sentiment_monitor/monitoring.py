from __future__ import annotations

import logging

from src.sentiment_monitor.config import AppConfig, get_config
from src.sentiment_monitor.text_cleaning import build_text_log_payload

try:
    from opencensus.ext.azure.log_exporter import AzureLogHandler
except ImportError:  # pragma: no cover - dépendance optionnelle hors Streamlit
    AzureLogHandler = None  # type: ignore[assignment]


LOGGER_NAME = "air_paradis_sentiment_monitor"


def _has_azure_handler(logger: logging.Logger) -> bool:
    if AzureLogHandler is None:
        return False
    return any(isinstance(handler, AzureLogHandler) for handler in logger.handlers)


def get_monitoring_logger(config: AppConfig | None = None) -> logging.Logger:
    """Retourne un logger idempotent, avec Azure App Insights si configuré."""
    active_config = config or get_config()
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if active_config.azure_connection_string and AzureLogHandler is not None:
        if not _has_azure_handler(logger):
            handler = AzureLogHandler(
                connection_string=active_config.azure_connection_string,
            )
            handler.setLevel(logging.INFO)
            logger.addHandler(handler)

    return logger


def build_monitoring_dimensions(
    tweet_text: str,
    class_id: int,
    label: str,
    probability: float | None = None,
    kind: str = "prediction",
    source: str = "streamlit",
    config: AppConfig | None = None,
) -> dict[str, object]:
    """Construit des dimensions sans exposer le tweet brut complet."""
    active_config = config or get_config()
    dimensions = {
        "kind": kind,
        "source": source,
        "prediction": int(class_id),
        "label": label,
        **build_text_log_payload(
            tweet_text,
            max_chars=active_config.tweet_preview_chars,
        ),
    }
    if probability is not None:
        dimensions["probability"] = float(probability)
    return dimensions


def log_prediction(
    tweet_text: str,
    class_id: int,
    label: str,
    probability: float | None = None,
    logger: logging.Logger | None = None,
    source: str = "streamlit",
) -> None:
    """Log une prédiction avec un aperçu de texte limité."""
    active_logger = logger or get_monitoring_logger()
    dimensions = build_monitoring_dimensions(
        tweet_text=tweet_text,
        class_id=class_id,
        label=label,
        probability=probability,
        kind="predict_api",
        source=source,
    )
    active_logger.info("predict_api", extra={"custom_dimensions": dimensions})


def log_bad_prediction(
    tweet_text: str,
    class_id: int,
    label: str,
    probability: float | None = None,
    logger: logging.Logger | None = None,
    source: str = "streamlit",
) -> None:
    """Log un signalement utilisateur avec un aperçu de texte limité."""
    active_logger = logger or get_monitoring_logger()
    dimensions = build_monitoring_dimensions(
        tweet_text=tweet_text,
        class_id=class_id,
        label=label,
        probability=probability,
        kind="bad_pred",
        source=source,
    )
    active_logger.warning("bad_pred", extra={"custom_dimensions": dimensions})
