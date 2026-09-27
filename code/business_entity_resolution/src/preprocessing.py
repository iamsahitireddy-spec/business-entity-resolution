"""Preprocessing Module for Business Entity Resolution.

Author: Anisa (Person 1 — Data Understanding, Preprocessing & EDA)

What this file does:
Cleans and standardizes company names, addresses, and country names so that
the matching models can easily compare them without getting confused by
capital letters, extra spaces, or punctuation marks like '&'.
"""

import re
import unicodedata
from typing import Any, List
import pandas as pd


def normalize_text(text: Any) -> str:
    """Cleans a single piece of text in 5 simple steps.

    Example:
        Input:  "  Acme & Sons, Inc.  "
        Output: "acme and sons inc"
    """
    # Step 1: If text is missing or blank, return empty text
    if text is None or pd.isna(text):
        return ""

    text = str(text).strip()
    if not text:
        return ""

    # Step 2: Clean special characters and accents (e.g., 'Café' becomes normal 'Cafe')
    text = unicodedata.normalize("NFKC", text)

    # Step 3: Make everything lowercase
    text = text.lower()

    # Step 4: Turn '&' into ' and '
    text = re.sub(r"&", " and ", text)

    # Step 5: Replace punctuation with spaces so words don't stick together
    # (e.g., "A/B" becomes "a b", not "ab")
    text = re.sub(r"[^\w\s]", " ", text)

    # Step 6: Collapse multiple spaces into one single space
    text = re.sub(r"\s+", " ", text).strip()

    return text


def normalize_business_name(name: Any) -> str:
    """Cleans a company name while keeping important tags like Inc, Ltd, LLC."""
    return normalize_text(name)


def normalize_address(address: Any) -> str:
    """Cleans a street address. If the address is missing, safely returns empty text."""
    return normalize_text(address)


def normalize_country(country: Any) -> str:
    """Cleans country names. Works for any country (US, India, France, etc.)."""
    return normalize_text(country)


def is_missing_address(address: Any) -> bool:
    """Checks whether an address is blank, empty, or missing."""
    if address is None or pd.isna(address):
        return True
    return str(address).strip() == ""


def tokenize_text(text: Any) -> List[str]:
    """Splits cleaned text into a simple list of separate words.

    Example:
        Input:  "acme and sons inc"
        Output: ["acme", "and", "sons", "inc"]
    """
    cleaned = normalize_text(text)
    if not cleaned:
        return []
    return cleaned.split()


def preprocess_dataframe(
    df: pd.DataFrame,
    name_col: str = "business_name",
    address_col: str = "business_address",
    country_col: str = "country",
) -> pd.DataFrame:
    """Cleans an entire table of business records.

    Keeps all original columns untouched (including entity_id) and adds 5 new columns:
      1. business_name_clean     -> Clean company name
      2. business_address_clean  -> Clean address (empty if missing)
      3. country_clean           -> Clean country
      4. business_name_tokens    -> List of words from the name
      5. business_address_tokens -> List of words from the address
    """
    # Make a copy so we don't accidentally change the original table
    clean_df = df.copy()

    # 1. Clean the business names
    if name_col in clean_df.columns:
        clean_df["business_name_clean"] = clean_df[name_col].apply(normalize_business_name)
    else:
        clean_df["business_name_clean"] = ""

    # 2. Clean the addresses (safely handles missing addresses)
    if address_col in clean_df.columns:
        clean_df["business_address_clean"] = clean_df[address_col].apply(normalize_address)
    else:
        clean_df["business_address_clean"] = ""

    # 3. Clean the countries
    if country_col in clean_df.columns:
        clean_df["country_clean"] = clean_df[country_col].apply(normalize_country)
    else:
        clean_df["country_clean"] = ""

    # 4. Create word lists for names and addresses
    clean_df["business_name_tokens"] = clean_df["business_name_clean"].apply(tokenize_text)
    clean_df["business_address_tokens"] = clean_df["business_address_clean"].apply(tokenize_text)

    return clean_df


if __name__ == "__main__":
    # Quick visual demonstration
    sample_records = pd.DataFrame({
        "entity_id": ["S1-101", "S1-102", "S1-103"],
        "business_name": ["Johnson & Johnson, LLC", "B+ Retail Inc.", "Café Paris"],
        "business_address": ["100 Main St., Suite #4", "", "12 Rue de Lyon"],
        "country": ["US", "US", "France"],
    })

    print("--- Before Cleaning ---")
    print(sample_records[["entity_id", "business_name", "business_address", "country"]])

    print("\n--- After Cleaning ---")
    result = preprocess_dataframe(sample_records)
    print(result[["entity_id", "business_name_clean", "business_address_clean", "country_clean"]])
