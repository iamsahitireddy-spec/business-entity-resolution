"""Business name text normalization module.

Provides reusable normalizers for raw business names, addressing variations in
legal suffixes (Corp vs Corporation, Pvt vs Private, Ltd vs Limited), punctuation,
casing, character transliteration, and whitespace inconsistencies.

Note:
    Care must be taken not to over-normalize text in a way that destroys essential
    distinguishing features between distinct business entities.
"""

import re
from typing import Optional
import pandas as pd


class BusinessNameNormalizer:
    """Normalizes raw business entity names for matching and candidate generation."""

    # Common legal suffix mappings across international business records
    LEGAL_SUFFIX_MAP = {
        r"\bcorp\b": "corporation",
        r"\binc\b": "incorporated",
        r"\bltd\b": "limited",
        r"\bpvt\b": "private",
        r"\bllc\b": "limited liability company",
        r"\bco\b": "company",
        r"\bcoop\b": "cooperative",
        r"\bsa\b": "sociedad anonima",
        r"\bsarl\b": "societe a responsabilite limitee",
    }

    def __init__(self, normalize_legal_suffixes: bool = True):
        """Initialize normalizer.

        Args:
            normalize_legal_suffixes: Whether to expand or standardize legal entity suffixes.
        """
        self.normalize_legal_suffixes = normalize_legal_suffixes

    def normalize(self, name: str) -> str:
        """Normalize a single raw business name string.

        Future steps to consider:
        1. Lowercasing
        2. Unicode normalization / ASCII transliteration (e.g. accents handling)
        3. Punctuation removal or standardization
        4. Standardizing common legal suffixes (Corp -> Corporation, Pvt -> Private, Ltd -> Limited)
        5. Extra whitespace stripping and collapsing

        Args:
            name: Raw business name string.

        Returns:
            Normalized business name string.
        """
        if not name or not isinstance(name, str):
            return ""

        # Step 1: Lowercase conversion
        cleaned = name.lower().strip()

        # Step 2: Basic punctuation & whitespace cleanup (placeholder logic)
        cleaned = re.sub(r"[^\w\s]", " ", cleaned)

        # Step 3: Legal suffix standardization (if enabled)
        if self.normalize_legal_suffixes:
            for pattern, replacement in self.LEGAL_SUFFIX_MAP.items():
                cleaned = re.sub(pattern, replacement, cleaned)

        # Step 4: Collapse multiple spaces
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        return cleaned

    def transform_dataframe(self, df: pd.DataFrame, name_col: str = "business_name") -> pd.DataFrame:
        """Apply normalization across a pandas DataFrame column.

        Args:
            df: Input DataFrame containing business records.
            name_col: Column name containing raw business names.

        Returns:
            DataFrame with added 'normalized_name' column.
        """
        result_df = df.copy()
        if name_col in result_df.columns:
            result_df["normalized_name"] = result_df[name_col].apply(self.normalize)
        else:
            raise KeyError(f"Column '{name_col}' not found in DataFrame.")
        return result_df
