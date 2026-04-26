import json
import logging
from pathlib import Path

from src.sentiment_monitor.config import AppConfig
from src.sentiment_monitor.monitoring import (
    LOGGER_NAME,
    LocalJsonlHandler,
    build_monitoring_dimensions,
    get_monitoring_logger,
    log_prediction,
)


def _reset_monitoring_logger() -> None:
    logger = logging.getLogger(LOGGER_NAME)
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()


def test_logger_uses_local_backend_by_default(tmp_path):
    _reset_monitoring_logger()
    local_path = tmp_path / "monitoring_events.jsonl"
    config = AppConfig(
        model_path=Path("models/tfidf_vectorizer.pkl"),
        azure_connection_string="",
        tweet_preview_chars=160,
        monitoring_backend="local",
        local_monitoring_path=local_path,
    )

    logger = get_monitoring_logger(config)

    assert logger.name == "air_paradis_sentiment_monitor"
    assert any(isinstance(handler, LocalJsonlHandler) for handler in logger.handlers)


def test_local_monitoring_writes_jsonl_event(tmp_path):
    _reset_monitoring_logger()
    local_path = tmp_path / "monitoring_events.jsonl"
    config = AppConfig(
        model_path=Path("models/tfidf_vectorizer.pkl"),
        azure_connection_string="",
        tweet_preview_chars=160,
        monitoring_backend="local",
        local_monitoring_path=local_path,
    )
    logger = get_monitoring_logger(config)

    log_prediction(
        tweet_text="Great flight and kind staff",
        class_id=1,
        label="Positif",
        probability=0.82,
        logger=logger,
        source="test",
    )

    lines = local_path.read_text(encoding="utf-8").splitlines()
    event = json.loads(lines[-1])

    assert event["event"] == "predict_api"
    assert event["level"] == "INFO"
    assert event["dimensions"]["source"] == "test"
    assert event["dimensions"]["label"] == "Positif"
    assert "tweet_text" not in event["dimensions"]


def test_local_monitoring_handler_is_not_duplicated(tmp_path):
    _reset_monitoring_logger()
    local_path = tmp_path / "monitoring_events.jsonl"
    config = AppConfig(
        model_path=Path("models/tfidf_vectorizer.pkl"),
        azure_connection_string="",
        tweet_preview_chars=160,
        monitoring_backend="local",
        local_monitoring_path=local_path,
    )

    logger = get_monitoring_logger(config)
    logger = get_monitoring_logger(config)

    local_handlers = [
        handler
        for handler in logger.handlers
        if isinstance(handler, LocalJsonlHandler)
    ]

    assert len(local_handlers) == 1


def test_monitoring_dimensions_do_not_include_raw_text():
    config = AppConfig(
        model_path=Path("models/tfidf_vectorizer.pkl"),
        azure_connection_string="",
        tweet_preview_chars=20,
        monitoring_backend="local",
        local_monitoring_path=Path("logs/monitoring_events.jsonl"),
    )

    dimensions = build_monitoring_dimensions(
        tweet_text="This is a very long tweet that should be truncated before logging",
        class_id=1,
        label="Positif",
        probability=0.91,
        config=config,
    )

    assert "tweet_text" not in dimensions
    assert len(str(dimensions["tweet_preview"])) <= 20
    assert dimensions["is_truncated"] is True
    assert dimensions["tweet_length"] > 20
