"""Country normalization module for Business Entity Resolution.

Author: Anisa (Person 1 — Data Understanding, Preprocessing & EDA)

Provides reusable, deterministic country normalizers.
Treats country as an open-set string field (e.g. US, India, France) without
hardcoding a fixed whitelist or rejecting unseen international countries.
"""

import re
import unicodedata
from typing import Any, Optional
import pandas as pd


class CountryNormalizer:
    """Normalizes country string fields across business records without hardcoding fixed country lists."""

    def __init__(self):
        """Initialize CountryNormalizer."""
        pass

    def normalize(self, country: Any) -> str:
        """Normalize a single country string deterministically.

        Steps:
        1. Safe null check (returns "" for None, NaN, empty strings)
        2. Unicode normalization (NFKC)
        3. Lowercase conversion
        4. Punctuation removal
        5. Whitespace stripping & collapsing

        Args:
            country: Raw country string or missing value.

        Returns:
            Normalized lowercase country string (e.g. 'us', 'india', 'france').
        """
        if country is None or pd.isna(country):
            return ""

        country_str = str(country).strip()
        if not country_str:
            return ""

        # Step 1: Unicode normalization
        cleaned = unicodedata.normalize("NFKC", country_str)

        # Step 2: Lowercase conversion
        cleaned = cleaned.lower()

        # Step 3: Remove punctuation
        cleaned = re.sub(r"[^\w\s]", " ", cleaned)

        # Step 4: Collapse whitespace
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        return cleaned

    def transform_dataframe(self, df: pd.DataFrame, country_col: str = "country") -> pd.DataFrame:
        """Apply country normalization across a pandas DataFrame column.

        Args:
            df: Input DataFrame containing business records.
            country_col: Column name containing raw country values.

        Returns:
            DataFrame with added 'normalized_country' column.
        """
        result_df = df.copy()
        if country_col in result_df.columns:
            result_df["normalized_country"] = result_df[country_col].apply(self.normalize)
        else:
            raise KeyError(f"Column '{country_col}' not found in DataFrame.")
        return result_df


# Module-level convenience function
def normalize_country(country: Any) -> str:
    """Convenience function to normalize a single country string."""
    return CountryNormalizer().normalize(country)


if __name__ == "__main__":
    normalizer = CountryNormalizer()
    test_countries = ["US", "  India  ", "France", "FRANCE", "United States", None, ""]
    print("Country Normalization Demonstration:")
    for c in test_countries:
        print(f"  Raw: {repr(c):<18} -> Normalized: {repr(normalizer.normalize(c))}")
