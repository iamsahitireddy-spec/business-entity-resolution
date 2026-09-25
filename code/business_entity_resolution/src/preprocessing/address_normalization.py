"""Business address normalization module.

Provides reusable normalizers for noisy business addresses.
Handles common address abbreviations, unit/suite numbers, formatting noise,
and street designation standardization.

IMPORTANT:
    External geocoding services, government databases, or external API lookups
    are STRICTLY PROHIBITED by competition rules. All address normalization must
    rely strictly on string transformation rules and local parsing.
"""

import re
import pandas as pd


class AddressNormalizer:
    """Normalizes raw business address strings without relying on external geocoding services."""

    # Common street and directional abbreviation mappings
    ADDRESS_ABBREVIATIONS = {
        r"\bst\b": "street",
        r"\bave\b": "avenue",
        r"\brd\b": "road",
        r"\bblvd\b": "boulevard",
        r"\bdr\b": "drive",
        r"\bln\b": "lane",
        r"\bpkwy\b": "parkway",
        r"\bste\b": "suite",
        r"\bapt\b": "apartment",
        r"\bfl\b": "floor",
        r"\bbldg\b": "building",
        r"\bpo box\b": "post office box",
    }

    def __init__(self, expand_abbreviations: bool = True):
        """Initialize AddressNormalizer.

        Args:
            expand_abbreviations: Whether to standardize common street abbreviations.
        """
        self.expand_abbreviations = expand_abbreviations

    def normalize(self, address: str) -> str:
        """Normalize a single address string.

        Future steps to consider:
        1. Lowercasing and strip leading/trailing whitespace
        2. Removing non-alphanumeric noise while preserving numbers & street words
        3. Standardizing street component abbreviations (e.g. St -> Street, Ave -> Avenue)
        4. Handling landmark-based or unstructured address tokens
        5. Collapsing multiple spaces

        Args:
            address: Raw business address string.

        Returns:
            Normalized address string.
        """
        if not address or not isinstance(address, str):
            return ""

        # Step 1: Lowercasing
        cleaned = address.lower().strip()

        # Step 2: Remove punctuation (except digits and words)
        cleaned = re.sub(r"[^\w\s]", " ", cleaned)

        # Step 3: Expand common street abbreviations if configured
        if self.expand_abbreviations:
            for pattern, replacement in self.ADDRESS_ABBREVIATIONS.items():
                cleaned = re.sub(pattern, replacement, cleaned)

        # Step 4: Collapse whitespace
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        return cleaned

    def transform_dataframe(self, df: pd.DataFrame, address_col: str = "business_address") -> pd.DataFrame:
        """Apply address normalization across a pandas DataFrame.

        Args:
            df: Input DataFrame containing address records.
            address_col: Name of column containing raw addresses.

        Returns:
            DataFrame with added 'normalized_address' column.
        """
        result_df = df.copy()
        if address_col in result_df.columns:
            result_df["normalized_address"] = result_df[address_col].apply(self.normalize)
        else:
            raise KeyError(f"Column '{address_col}' not found in DataFrame.")
        return result_df
