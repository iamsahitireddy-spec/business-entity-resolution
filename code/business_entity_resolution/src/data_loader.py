"""Data loading utilities for the Business Entity Resolution dataset.

Handles loading tab-separated value (TSV) dataset files for Source 1,
Source 2, Source 3, and ground truth files without hardcoding comma separators.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd

from src.config import config


class DataLoader:
    """Loader for entity resolution TSV datasets."""

    def __init__(self, data_dir: Optional[Union[str, Path]] = None):
        """Initialize DataLoader with a target data directory.

        Args:
            data_dir: Path to directory containing source TSV files. Defaults to config.TRAIN_DIR.
        """
        self.data_dir = Path(data_dir) if data_dir else config.TRAIN_DIR

    def load_tsv(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """Load a single TSV file using tab separation.

        Args:
            file_path: Path to the TSV file.

        Returns:
            pd.DataFrame containing file contents.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"TSV dataset file not found at: {path}")

        # ALWAYS read dataset files with tab separator
        df = pd.read_csv(path, sep=config.DELIMITER, dtype=str)
        df.fillna("", inplace=True)
        return df

    def load_source1(self, split: str = "train") -> pd.DataFrame:
        """Load Source 1 reference records (S1- prefix).

        Args:
            split: 'train' or 'test'.

        Returns:
            DataFrame containing Source 1 records.
        """
        path = (config.TRAIN_DIR if split == "train" else config.TEST_DIR) / f"{split}_source1.tsv"
        return self.load_tsv(path)

    def load_source2(self, split: str = "train") -> pd.DataFrame:
        """Load Source 2 noisy records (S2- prefix).

        Args:
            split: 'train' or 'test'.

        Returns:
            DataFrame containing Source 2 records.
        """
        path = (config.TRAIN_DIR if split == "train" else config.TEST_DIR) / f"{split}_source2.tsv"
        return self.load_tsv(path)

    def load_source3(self, split: str = "train") -> pd.DataFrame:
        """Load Source 3 noisy records (S3- prefix).

        Args:
            split: 'train' or 'test'.

        Returns:
            DataFrame containing Source 3 records.
        """
        path = (config.TRAIN_DIR if split == "train" else config.TEST_DIR) / f"{split}_source3.tsv"
        return self.load_tsv(path)

    def load_ground_truth(self, train_dir: Optional[Union[str, Path]] = None) -> pd.DataFrame:
        """Load ground truth training labels.

        Ground truth format:
            source1_entity_id | matched_entity_ids
            S1-1001           | S2-5002,S3-9001
            S1-1002           |

        Args:
            train_dir: Directory containing train_ground_truth.tsv.

        Returns:
            DataFrame containing ground truth mappings.
        """
        target_dir = Path(train_dir) if train_dir else config.TRAIN_DIR
        path = target_dir / config.GROUND_TRUTH_FILENAME
        df = self.load_tsv(path)
        return df

    def load_all_sources(self, split: str = "train") -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load all three source dataframes for a given split.

        Args:
            split: 'train' or 'test'.

        Returns:
            Tuple of (source1_df, source2_df, source3_df).
        """
        s1 = self.load_source1(split)
        s2 = self.load_source2(split)
        s3 = self.load_source3(split)
        return s1, s2, s3


def parse_matched_ids(matched_str: str) -> List[str]:
    """Helper function to parse comma-separated matched entity IDs string into a list.

    Args:
        matched_str: Comma-separated ID string (e.g. "S2-101,S3-205" or "").

    Returns:
        List of individual entity ID strings.
    """
    if not isinstance(matched_str, str) or not matched_str.strip():
        return []
    return [eid.strip() for eid in matched_str.split(",") if eid.strip()]
