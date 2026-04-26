from __future__ import annotations


def normalize_whitespace(text: str) -> str:
    """Normalise uniquement les espaces, sans modifier le sens du tweet."""
    return " ".join(str(text).split())


def truncate_text(text: str, max_chars: int = 160) -> tuple[str, bool]:
    """Retourne un aperçu borné du texte et indique s'il a été tronqué."""
    cleaned = normalize_whitespace(text)
    if len(cleaned) <= max_chars:
        return cleaned, False
    if max_chars <= 3:
        return cleaned[:max_chars], True
    return f"{cleaned[: max_chars - 3].rstrip()}...", True


def build_text_log_payload(text: str, max_chars: int = 160) -> dict[str, object]:
    """Prépare les champs sûrs à envoyer dans les logs de monitoring."""
    cleaned = normalize_whitespace(text)
    preview, is_truncated = truncate_text(cleaned, max_chars=max_chars)
    return {
        "tweet_preview": preview,
        "tweet_length": len(cleaned),
        "is_truncated": is_truncated,
    }
