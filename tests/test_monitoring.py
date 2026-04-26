from pathlib import Path

from src.sentiment_monitor.config import AppConfig
from src.sentiment_monitor.monitoring import (
    build_monitoring_dimensions,
    get_monitoring_logger,
)


def test_logger_without_azure_connection_string():
    config = AppConfig(
        model_path=Path("models/tfidf_vectorizer.pkl"),
        azure_connection_string="",
        tweet_preview_chars=160,
    )

    logger = get_monitoring_logger(config)

    assert logger.name == "air_paradis_sentiment_monitor"


def test_monitoring_dimensions_do_not_include_raw_text():
    config = AppConfig(
        model_path=Path("models/tfidf_vectorizer.pkl"),
        azure_connection_string="",
        tweet_preview_chars=20,
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
