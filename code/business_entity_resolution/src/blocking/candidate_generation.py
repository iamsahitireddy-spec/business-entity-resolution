"""Blocking and candidate generation module.

Responsible for generating candidate pairs between Source 1 (reference source)
and Source 2 / Source 3 noisy business records.

Blocking drastically reduces the $O(N_1 \times (N_2 + N_3))$ search space to a manageable
set of high-probability candidate pairs for ML scoring.

CRITICAL COMPETITION RULE:
    Every final match predicted in matching_results.tsv MUST be present within candidate_pairs.tsv.
"""

from pathlib import Path
from typing import Dict, List, Optional, Set, Union
import pandas as pd

from src.config import config


class CandidateGenerator:
    """Generates candidate entity pairs between Source 1 and Source 2 / Source 3."""

    def __init__(self, top_k: int = 50, similarity_threshold: float = 0.3):
        """Initialize CandidateGenerator with configurable blocking parameters.

        Args:
            top_k: Maximum number of candidate matches retained per Source 1 entity.
            similarity_threshold: Minimum similarity threshold for candidate selection.
        """
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def generate_candidates(
        self,
        source1_df: pd.DataFrame,
        source2_df: pd.DataFrame,
        source3_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Generate candidate pairs for every Source 1 entity.

        Candidate Blocking Strategies to implement:
        1. Exact token matching (e.g. key name tokens, first word, zip/city)
        2. Open-set Country filtering / grouping (only compare matching countries if present)
        3. TF-IDF vector similarity top-K retrieval (N-gram characters / word tokens)
        4. MinHash / Locality Sensitive Hashing (LSH) for scalable blocking

        Args:
            source1_df: Source 1 entity DataFrame.
            source2_df: Source 2 entity DataFrame.
            source3_df: Source 3 entity DataFrame.

        Returns:
            DataFrame with columns:
                - source1_entity_id: S1 ID string
                - candidate_entity_ids: comma-separated list of candidate S2/S3 IDs
        """
        # Placeholder skeleton structure for candidate generation logic
        candidate_rows = []

        for s1_id in source1_df[config.COL_ENTITY_ID]:
            # Future implementation: perform fast indexing / nearest neighbor lookup
            # to retrieve candidate S2 and S3 IDs for s1_id
            candidates_for_s1: List[str] = []

            candidate_rows.append({
                config.COL_S1_ID: s1_id,
                config.COL_CANDIDATE_IDS: ",".join(candidates_for_s1),
            })

        candidate_pairs_df = pd.DataFrame(candidate_rows)
        return candidate_pairs_df

    def save_candidate_pairs(
        self,
        candidate_pairs_df: pd.DataFrame,
        output_path: Optional[Union[str, Path]] = None,
    ) -> Path:
        """Save candidate pairs DataFrame to candidate_pairs.tsv.

        Args:
            candidate_pairs_df: DataFrame containing source1_entity_id and candidate_entity_ids.
            output_path: Target path. Defaults to output/candidate_pairs.tsv.

        Returns:
            Path object pointing to saved TSV file.
        """
        target_path = Path(output_path) if output_path else config.OUTPUT_DIR / config.CANDIDATE_PAIRS_FILENAME
        target_path.parent.mkdir(parents=True, exist_ok=True)

        candidate_pairs_df.to_csv(target_path, sep=config.DELIMITER, index=False)
        return target_path
