"""Exploratory Data Analysis (EDA) Module for Business Entity Resolution.

Author: Anisa (Person 1 — Data Understanding, Preprocessing & EDA)

What this file does:
Provides simple, reusable tools to inspect and understand our dataset files:
  - Table sizes (row and column counts)
  - Missing or blank values (like missing addresses)
  - Duplicate company IDs
  - Country shares (US, India, France)
  - Average word and character lengths
  - Ground truth answer key patterns (singletons, match counts)
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union
import numpy as np
import pandas as pd


def get_dataset_summary(df: pd.DataFrame, dataset_name: str = "Dataset") -> Dict[str, Any]:
    """Returns basic information about a table: row count, columns, and memory size."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df).__name__}")

    memory_mb = round(float(df.memory_usage(deep=True).sum()) / (1024 * 1024), 2)

    return {
        "name": dataset_name,
        "num_rows": int(len(df)),
        "num_columns": int(len(df.columns)),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "memory_mb": memory_mb,
    }


def get_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Checks every column in a table for blank, empty, or missing values."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df).__name__}")

    total_rows = len(df)
    results = []

    for col in df.columns:
        # Check standard nulls (None / NaN)
        is_null = df[col].isna()
        null_count = int(is_null.sum())

        # Check empty text strings ("")
        non_null_text = df.loc[~is_null, col].astype(str)
        empty_str_count = int((non_null_text.str.strip() == "").sum())

        total_missing = null_count + empty_str_count
        missing_pct = round((total_missing / total_rows * 100), 2) if total_rows > 0 else 0.0

        results.append({
            "column": col,
            "null_count": null_count,
            "empty_str_count": empty_str_count,
            "total_missing": total_missing,
            "missing_percentage": missing_pct,
            "non_missing_count": total_rows - total_missing,
        })

    return pd.DataFrame(results)


def get_duplicate_stats(
    df: pd.DataFrame,
    id_col: str = "entity_id",
    subset: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Checks if there are any duplicate company IDs or duplicate records."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df).__name__}")

    total_rows = len(df)

    # 1. Check duplicate IDs
    if id_col in df.columns:
        dup_ids = int(df.duplicated(subset=[id_col], keep=False).sum())
        dup_id_pct = round((dup_ids / total_rows * 100), 2) if total_rows > 0 else 0.0
    else:
        dup_ids = 0
        dup_id_pct = 0.0

    # 2. Check identical full rows
    exact_dup_rows = int(df.duplicated(keep=False).sum())

    # 3. Check records with identical name + address + country
    if subset is None:
        subset = [c for c in ["business_name", "business_address", "country"] if c in df.columns]

    attr_dup_records = int(df.duplicated(subset=subset, keep=False).sum()) if subset else 0

    return {
        "total_rows": total_rows,
        "duplicate_ids_count": dup_ids,
        "duplicate_ids_percentage": dup_id_pct,
        "exact_duplicate_rows_count": exact_dup_rows,
        "attribute_duplicate_records_count": attr_dup_records,
        "attribute_subset_evaluated": subset or [],
    }


def get_country_distribution(
    df: pd.DataFrame,
    country_col: str = "country",
) -> pd.DataFrame:
    """Counts how many companies belong to each country (e.g., US, India, France)."""
    if not isinstance(df, pd.DataFrame) or country_col not in df.columns:
        return pd.DataFrame(columns=["country", "count", "percentage", "cumulative_percentage"])

    total_rows = len(df)
    if total_rows == 0:
        return pd.DataFrame(columns=["country", "count", "percentage", "cumulative_percentage"])

    clean_countries = df[country_col].fillna("").astype(str).str.strip().replace("", "<MISSING>")
    counts = clean_countries.value_counts().reset_index()
    counts.columns = ["country", "count"]
    counts["percentage"] = (counts["count"] / total_rows * 100).round(2)
    counts["cumulative_percentage"] = counts["percentage"].cumsum().round(2)

    return counts


def get_text_length_statistics(
    df: pd.DataFrame,
    name_col: str = "business_name",
    address_col: str = "business_address",
) -> pd.DataFrame:
    """Calculates average character and word counts for company names and addresses."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df).__name__}")

    data: Dict[str, Any] = {}

    if name_col in df.columns:
        names = df[name_col].fillna("").astype(str).str.strip()
        data["name_char_length"] = names.str.len()
        data["name_word_count"] = names.apply(lambda s: len(s.split()) if s else 0)

    if address_col in df.columns:
        addresses = df[address_col].fillna("").astype(str).str.strip()
        data["address_char_length"] = addresses.str.len()
        data["address_word_count"] = addresses.apply(lambda s: len(s.split()) if s else 0)

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data).describe().round(2)


def get_ground_truth_match_counts(
    gt_df: pd.DataFrame,
    s1_col: str = "source1_entity_id",
    matched_col: str = "matched_entity_ids",
) -> Dict[str, Any]:
    """Analyzes the answer key to see how many companies have matches vs zero matches."""
    if not isinstance(gt_df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(gt_df).__name__}")

    total_s1 = len(gt_df)
    if total_s1 == 0:
        return {"total_s1_entities": 0, "singleton_count": 0, "matched_entities_count": 0}

    # Count matches per Source 1 entity
    def count_matches(val: str) -> List[str]:
        if not val or not str(val).strip():
            return []
        return [eid.strip() for eid in str(val).split(",") if eid.strip()]

    parsed = gt_df[matched_col].apply(count_matches)
    lengths = parsed.apply(len)

    singletons = int((lengths == 0).sum())
    matched_s1 = total_s1 - singletons

    s2_count = sum(sum(1 for eid in ids if eid.startswith("S2-")) for ids in parsed)
    s3_count = sum(sum(1 for eid in ids if eid.startswith("S3-")) for ids in parsed)

    # Match counts breakdown (0 matches, 1 match, 2 matches, 3 matches, 4 matches, 5+)
    raw_counts = lengths.value_counts().to_dict()
    cardinality: Dict[str, int] = {}
    for c in sorted(raw_counts.keys()):
        key = str(c) if c < 5 else "5+"
        cardinality[key] = cardinality.get(key, 0) + raw_counts[c]

    return {
        "total_s1_entities": total_s1,
        "singleton_count": singletons,
        "singleton_percentage": round(singletons / total_s1 * 100, 2),
        "matched_entities_count": matched_s1,
        "matched_entities_percentage": round(matched_s1 / total_s1 * 100, 2),
        "total_matches_count": int(lengths.sum()),
        "s2_matches_count": s2_count,
        "s3_matches_count": s3_count,
        "cardinality_distribution": cardinality,
        "max_matches_per_entity": int(lengths.max()),
        "mean_matches_per_entity": round(float(lengths.mean()), 2),
    }


def run_full_eda(
    data_dict: Dict[str, pd.DataFrame],
    ground_truth_df: Optional[pd.DataFrame] = None,
) -> Dict[str, Any]:
    """Runs all EDA functions across a dictionary of tables."""
    results: Dict[str, Any] = {}

    for name, df in data_dict.items():
        results[name] = {
            "summary": get_dataset_summary(df, dataset_name=name),
            "missing_values": get_missing_values(df),
            "duplicates": get_duplicate_stats(df),
            "country_distribution": get_country_distribution(df),
            "text_length_stats": get_text_length_statistics(df),
        }

    if ground_truth_df is not None:
        results["ground_truth"] = {
            "summary": get_dataset_summary(ground_truth_df, dataset_name="ground_truth"),
            "missing_values": get_missing_values(ground_truth_df),
            "match_counts": get_ground_truth_match_counts(ground_truth_df),
        }

    return results


def analyze_source_file_stream(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Memory-friendly reader: reads large source TSVs line by line without crashing."""
    import csv
    from collections import Counter

    path = Path(file_path)
    total_rows = 0
    missing = {"entity_id": 0, "business_name": 0, "business_address": 0, "country": 0}
    countries: Counter = Counter()
    seen_ids: Set[str] = set()
    dup_ids = 0

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)  # Skip header

        for row in reader:
            if not row:
                continue
            total_rows += 1
            if len(row) < 4:
                row += [""] * (4 - len(row))

            eid, name, addr, country = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()

            if eid in seen_ids:
                dup_ids += 1
            else:
                seen_ids.add(eid)

            if not eid: missing["entity_id"] += 1
            if not name: missing["business_name"] += 1
            if not addr: missing["business_address"] += 1
            if not country: missing["country"] += 1

            countries[country if country else "<MISSING>"] += 1

    return {
        "file_name": path.name,
        "total_rows": total_rows,
        "duplicate_ids": dup_ids,
        "missing_counts": missing,
        "country_distribution": dict(countries),
    }


def analyze_ground_truth_file_stream(gt_path: Union[str, Path]) -> Dict[str, Any]:
    """Memory-friendly reader: reads large ground-truth TSVs line by line."""
    import csv
    from collections import Counter

    path = Path(gt_path)
    total_s1 = 0
    singletons = 0
    s2_matches = 0
    s3_matches = 0
    cardinality: Counter = Counter()

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)

        for row in reader:
            if not row:
                continue
            total_s1 += 1
            if len(row) < 2 or not row[1].strip():
                singletons += 1
                cardinality[0] += 1
            else:
                eids = [x.strip() for x in row[1].split(",") if x.strip()]
                cardinality[len(eids)] += 1
                for eid in eids:
                    if eid.startswith("S2-"): s2_matches += 1
                    elif eid.startswith("S3-"): s3_matches += 1

    return {
        "file_name": path.name,
        "total_s1_entities": total_s1,
        "singleton_count": singletons,
        "singleton_percentage": round(singletons / total_s1 * 100, 2) if total_s1 > 0 else 0.0,
        "matched_s1_count": total_s1 - singletons,
        "total_matches": s2_matches + s3_matches,
        "s2_matches": s2_matches,
        "s3_matches": s3_matches,
    }


if __name__ == "__main__":
    demo = pd.DataFrame({
        "entity_id": ["S1-1", "S1-2"],
        "business_name": ["Apex Logistics Inc", "Beta Technologies"],
        "business_address": ["100 Main St", ""],
        "country": ["US", "France"],
    })
    print("=== Simple EDA Demonstration ===")
    print("Table Summary:", get_dataset_summary(demo, "Demo Table")["num_rows"], "rows")
    print("Missing Addresses:\n", get_missing_values(demo)[["column", "total_missing"]])
