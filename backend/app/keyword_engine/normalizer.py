import re
from typing import Tuple, Optional
from app.keyword_engine.dictionary import TECH_KEYWORD_DICTIONARY


class KeywordNormalizer:
    """Normalizes raw input text and maps matched patterns to canonical tech keywords."""

    @staticmethod
    def normalize_text(text: str) -> str:
        """Lowercases and cleans whitespace for string matching."""
        if not text:
            return ""
        return text.lower()

    @staticmethod
    def resolve_canonical(pattern: str) -> Tuple[str, str]:
        """Map raw pattern/alias to (Canonical Name, Category)."""
        lower = pattern.lower().strip()
        if lower in TECH_KEYWORD_DICTIONARY:
            return TECH_KEYWORD_DICTIONARY[lower]

        # Capitalize fallback
        return lower.title(), "general_tech"


normalizer = KeywordNormalizer()
