"""Data Validation Module for Business Entity Resolution.

Author: Anisa (Person 1 — Data Understanding, Preprocessing & EDA)

What this file does:
Performs 2 simple safety checks on the raw dataset files:
  1. Prefix Check: Verifies that every ID starts with the correct letters (S1-, S2-, S3-).
  2. Reference Check: Verifies that every match listed in the answer key actually exists
     in our datasets (no ghost or missing IDs).
"""

import csv
from pathlib import Path
from typing import Any, Dict, List, Set, Union


def validate_id_prefix(
    file_path: Union[str, Path],
    expected_prefix: str,
) -> Dict[str, Any]:
    """Checks that every ID in a TSV file starts with the expected prefix (like 'S1-')."""
    path = Path(file_path)
    total_rows = 0
    valid_count = 0
    bad_ids: List[str] = []

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)  # Skip table header

        for row in reader:
            if not row:
                continue
            total_rows += 1
            entity_id = row[0].strip()

            if entity_id.startswith(expected_prefix):
                valid_count += 1
            else:
                if len(bad_ids) < 5:
                    bad_ids.append(entity_id)

    is_all_valid = (valid_count == total_rows)
    return {
        "file_name": path.name,
        "total_rows": total_rows,
        "expected_prefix": expected_prefix,
        "valid_prefix_count": valid_count,
        "invalid_prefix_count": total_rows - valid_count,
        "is_valid": is_all_valid,
        "sample_invalid_ids": bad_ids,
    }


def validate_ground_truth_references(
    gt_path: Union[str, Path],
    s1_path: Union[str, Path],
    s2_path: Union[str, Path],
    s3_path: Union[str, Path],
) -> Dict[str, Any]:
    """Checks that every company ID in the ground truth answer key really exists in the sources."""
    # 1. Read ground truth and collect all company IDs mentioned
    s1_needed: Set[str] = set()
    s2_needed: Set[str] = set()
    s3_needed: Set[str] = set()

    with open(gt_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)  # Skip header
        for row in reader:
            if not row:
                continue
            s1_id = row[0].strip()
            s1_needed.add(s1_id)

            if len(row) > 1 and row[1].strip():
                for match_id in row[1].split(","):
                    match_id = match_id.strip()
                    if match_id.startswith("S2-"):
                        s2_needed.add(match_id)
                    elif match_id.startswith("S3-"):
                        s3_needed.add(match_id)

    # 2. Check if S1 IDs exist in Source 1
    s1_missing = set(s1_needed)
    with open(s1_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)
        for row in reader:
            if row:
                s1_missing.discard(row[0].strip())

    # 3. Check if S2 IDs exist in Source 2
    s2_missing = set(s2_needed)
    with open(s2_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)
        for row in reader:
            if row:
                s2_missing.discard(row[0].strip())

    # 4. Check if S3 IDs exist in Source 3
    s3_missing = set(s3_needed)
    with open(s3_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)
        for row in reader:
            if row:
                s3_missing.discard(row[0].strip())

    all_valid = (len(s1_missing) == 0 and len(s2_missing) == 0 and len(s3_missing) == 0)

    return {
        "source1": {"referenced": len(s1_needed), "missing": len(s1_missing), "is_valid": len(s1_missing) == 0},
        "source2": {"referenced": len(s2_needed), "missing": len(s2_missing), "is_valid": len(s2_missing) == 0},
        "source3": {"referenced": len(s3_needed), "missing": len(s3_missing), "is_valid": len(s3_missing) == 0},
        "overall_integrity_valid": all_valid,
    }


def run_full_validation(train_dir: Union[str, Path]) -> Dict[str, Any]:
    """Runs all checks on the entire training folder."""
    train_path = Path(train_dir)
    s1_file = train_path / "train_source1.tsv"
    s2_file = train_path / "train_source2.tsv"
    s3_file = train_path / "train_source3.tsv"
    gt_file = train_path / "train_ground_truth.tsv"

    # Run prefix checks
    prefixes = {
        "source1": validate_id_prefix(s1_file, "S1-"),
        "source2": validate_id_prefix(s2_file, "S2-"),
        "source3": validate_id_prefix(s3_file, "S3-"),
    }

    # Run reference checks
    refs = validate_ground_truth_references(gt_file, s1_file, s2_file, s3_file)

    all_prefixes_ok = all(p["is_valid"] for p in prefixes.values())
    is_everything_ok = all_prefixes_ok and refs["overall_integrity_valid"]

    return {
        "prefix_validation": prefixes,
        "reference_validation": refs,
        "overall_valid": is_everything_ok,
    }


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    train_folder = repo_root / "dataset" / "train"
    print(f"Checking files in: {train_folder}")
    result = run_full_validation(train_folder)
    print(f"Are all files valid? -> {result['overall_valid']}")
