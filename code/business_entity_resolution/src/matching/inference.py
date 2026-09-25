"""Inference module for post-processing candidate match scores into final outputs.

Converts raw candidate pair predictions into formatted submission outputs
(matching_results.tsv) adhering to competition rules:
1. Exactly one row per Source 1 entity.
2. Only S2/S3 IDs in matched_entity_ids column.
3. Comma-separated IDs with no duplicates.
4. Empty string for singletons / non-matching entities.
"""

from pathlib import Path
from typing import Dict, List, Optional, Union
import pandas as pd

from src.config import config


class MatchPredictor:
    """Predicts entity matches and formats final matching_results.tsv output."""

    def __init__(self, match_threshold: float = 0.7):
        """Initialize MatchPredictor.

        Args:
            match_threshold: Probability decision threshold optimized for Macro F0.5.
                             Higher threshold enforces precision over recall.
        """
        self.match_threshold = match_threshold

    def generate_matching_results(
        self,
        source1_ids: List[str],
        pair_predictions_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Aggregate pairwise predictions into final matching_results.tsv DataFrame.

        Rules enforced:
        - Exactly one row for EVERY Source 1 entity.
        - matched_entity_ids contains only S2/S3 IDs.
        - Comma-separated list with no duplicate IDs.
        - Empty string for singletons.

        Args:
            source1_ids: Comprehensive list of all Source 1 entity IDs in the split.
            pair_predictions_df: DataFrame containing columns:
                                 ['source1_entity_id', 'candidate_entity_id', 'score']

        Returns:
            DataFrame with columns: ['source1_entity_id', 'matched_entity_ids']
        """
        # Map source1_entity_id -> list of selected match IDs
        matches_dict: Dict[str, List[str]] = {s1_id: [] for s1_id in source1_ids}

        if not pair_predictions_df.empty:
            # Filter candidate pairs exceeding precision-heavy decision threshold
            filtered_df = pair_predictions_df[pair_predictions_df["score"] >= self.match_threshold]

            for _, row in filtered_df.iterrows():
                s1_id = row["source1_entity_id"]
                cand_id = row["candidate_entity_id"]

                if s1_id in matches_dict:
                    # Prevent duplicate IDs
                    if cand_id not in matches_dict[s1_id]:
                        matches_dict[s1_id].append(cand_id)

        # Build output DataFrame ensuring exact row count matching source1_ids
        output_rows = [
            {
                config.COL_S1_ID: s1_id,
                config.COL_MATCHED_IDS: ",".join(matches_dict[s1_id]),
            }
            for s1_id in source1_ids
        ]

        return pd.DataFrame(output_rows)

    def save_matching_results(
        self,
        matching_results_df: pd.DataFrame,
        output_path: Optional[Union[str, Path]] = None,
    ) -> Path:
        """Save formatted matching results to matching_results.tsv.

        Args:
            matching_results_df: DataFrame containing source1_entity_id and matched_entity_ids.
            output_path: Path destination. Defaults to output/matching_results.tsv.

        Returns:
            Path object pointing to saved TSV file.
        """
        target_path = Path(output_path) if output_path else config.OUTPUT_DIR / config.MATCHING_RESULTS_FILENAME
        target_path.parent.mkdir(parents=True, exist_ok=True)

        matching_results_df.to_csv(target_path, sep=config.DELIMITER, index=False)
        return target_path
