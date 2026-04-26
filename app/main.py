"""Compatibilité avec l'ancien entrypoint `app.main:app`."""

from api.main import app

__all__ = ["app"]
