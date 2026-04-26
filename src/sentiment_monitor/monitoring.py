from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from pathlib import Path

from src.sentiment_monitor.config import AppConfig, get_config
from src.sentiment_monitor.text_cleaning import build_text_log_payload

try:
    from opencensus.ext.azure.log_exporter import AzureLogHandler
except ImportError:  # pragma: no cover - dépendance optionnelle hors Streamlit
    AzureLogHandler = None  # type: ignore[assignment]


LOGGER_NAME = "air_paradis_sentiment_monitor"


class LocalJsonlHandler(logging.Handler):
    """Handler local maison pour écrire les événements de monitoring en JSONL."""

    def __init__(self, path: Path) -> None:
        super().__init__(level=logging.INFO)
        self.path = Path(path)

    def emit(self, record: logging.LogRecord) -> None:
        event = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
            "dimensions": getattr(record, "custom_dimensions", {}),
        }
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")
        except Exception:  # pragma: no cover - garde-fou standard logging
            self.handleError(record)


def _same_path(left: Path, right: Path) -> bool:
    return Path(left).resolve() == Path(right).resolve()


def _has_local_handler(logger: logging.Logger, path: Path) -> bool:
    return any(
        isinstance(handler, LocalJsonlHandler) and _same_path(handler.path, path)
        for handler in logger.handlers
    )


def _remove_local_handlers(logger: logging.Logger, keep_path: Path | None = None) -> None:
    for handler in list(logger.handlers):
        if isinstance(handler, LocalJsonlHandler) and (
            keep_path is None or not _same_path(handler.path, keep_path)
        ):
            logger.removeHandler(handler)
            handler.close()


def _has_azure_handler(logger: logging.Logger) -> bool:
    if AzureLogHandler is None:
        return False
    return any(isinstance(handler, AzureLogHandler) for handler in logger.handlers)


def _remove_azure_handlers(logger: logging.Logger) -> None:
    if AzureLogHandler is None:
        return
    for handler in list(logger.handlers):
        if isinstance(handler, AzureLogHandler):
            logger.removeHandler(handler)
            handler.close()


def _ensure_null_handler(logger: logging.Logger) -> None:
    if not logger.handlers:
        logger.addHandler(logging.NullHandler())


def get_monitoring_logger(config: AppConfig | None = None) -> logging.Logger:
    """Retourne un logger idempotent, avec monitoring local et/ou Azure."""
    active_config = config or get_config()
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    backend = active_config.monitoring_backend
    local_enabled = backend in {"local", "both"}
    azure_enabled = backend in {"azure", "both"}

    if local_enabled:
        _remove_local_handlers(logger, keep_path=active_config.local_monitoring_path)
        if not _has_local_handler(logger, active_config.local_monitoring_path):
            logger.addHandler(LocalJsonlHandler(active_config.local_monitoring_path))
    else:
        _remove_local_handlers(logger)

    if azure_enabled and active_config.azure_connection_string and AzureLogHandler is not None:
        if not _has_azure_handler(logger):
            handler = AzureLogHandler(
                connection_string=active_config.azure_connection_string,
            )
            handler.setLevel(logging.INFO)
            logger.addHandler(handler)
    else:
        _remove_azure_handlers(logger)

    _ensure_null_handler(logger)

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
