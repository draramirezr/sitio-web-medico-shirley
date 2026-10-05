"""DGII e-CF helpers — Phase A/B."""

# Keep package import lightweight (avoid pulling signxml on every route).
from .config import get_ambiente, get_urls

__all__ = ["get_ambiente", "get_urls"]
