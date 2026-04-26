from src.sentiment_monitor.text_cleaning import (
    build_text_log_payload,
    normalize_whitespace,
    truncate_text,
)


def test_normalize_whitespace():
    assert normalize_whitespace("  hello    world  ") == "hello world"


def test_truncate_text_keeps_max_length():
    preview, is_truncated = truncate_text("abcdefghijklmnopqrstuvwxyz", max_chars=10)

    assert preview == "abcdefg..."
    assert len(preview) == 10
    assert is_truncated is True


def test_build_text_log_payload():
    payload = build_text_log_payload("  short   tweet  ", max_chars=160)

    assert payload == {
        "tweet_preview": "short tweet",
        "tweet_length": 11,
        "is_truncated": False,
    }
