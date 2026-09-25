"""Evaluation module implementing the competition's Macro-averaged F0.5 metric.

Evaluates validation predictions against ground truth labels, carefully handling
singletons (Source 1 records with zero matches) and precision-heavy weighting:

    F0.5 = (1.25 * Precision * Recall) / (0.25 * Precision + Recall)

Singleton evaluation rules:
- True singleton with empty prediction (no matches predicted): F0.5 = 1.0
- True singleton with non-empty prediction (false merge): F0.5 = 0.0
"""

from typing import Dict, List, Set, Tuple, Union
import numpy as np
import pandas as pd

from src.data_loader import parse_matched_ids
from src.config import config


def calculate_entity_f05(true_matches: Set[str], pred_matches: Set[str]) -> Tuple[float, float, float]:
    """Calculate Precision, Recall, and F0.5 score for a single Source 1 entity.

    Args:
        true_matches: Set of ground truth matching entity IDs.
        pred_matches: Set of predicted matching entity IDs.

    Returns:
        Tuple of (precision, recall, f0.5_score).
    """
    # Case 1: True Singleton (Ground truth has no matches)
    if not true_matches:
        if not pred_matches:
            # Correctly predicted singleton
            return 1.0, 1.0, 1.0
        else:
            # False merge assigned to a singleton
            return 0.0, 0.0, 0.0

    # Case 2: Entity has ground truth matches, but prediction is empty
    if not pred_matches:
        return 0.0, 0.0, 0.0

    # Case 3: Both sets are non-empty
    true_positives = len(true_matches.intersection(pred_matches))
    precision = true_positives / len(pred_matches)
    recall = true_positives / len(true_matches)

    denom = (0.25 * precision) + recall
    if denom == 0:
        f05 = 0.0
    else:
        f05 = (1.25 * precision * recall) / denom

    return precision, recall, f05


def calculate_macro_f05(
    ground_truth_df: pd.DataFrame,
    predictions_df: pd.DataFrame,
) -> Dict[str, float]:
    """Calculate Macro-averaged Precision, Recall, and F0.5 across all Source 1 entities.

    Args:
        ground_truth_df: DataFrame with ['source1_entity_id', 'matched_entity_ids'].
        predictions_df: DataFrame with ['source1_entity_id', 'matched_entity_ids'].

    Returns:
        Dictionary containing 'macro_precision', 'macro_recall', and 'macro_f05'.
    """
    # Index predictions by source1_entity_id
    pred_map = {}
    for _, row in predictions_df.iterrows():
        s1_id = row[config.COL_S1_ID]
        pred_map[s1_id] = set(parse_matched_ids(row[config.COL_MATCHED_IDS]))

    precisions = []
    recalls = []
    f05_scores = []

    for _, row in ground_truth_df.iterrows():
        s1_id = row[config.COL_S1_ID]
        gt_matches = set(parse_matched_ids(row[config.COL_MATCHED_IDS]))
        pred_matches = pred_map.get(s1_id, set())

        p, r, f05 = calculate_entity_f05(gt_matches, pred_matches)
        precisions.append(p)
        recalls.append(r)
        f05_scores.append(f05)

    return {
        "macro_precision": float(np.mean(precisions)) if precisions else 0.0,
        "macro_recall": float(np.mean(recalls)) if recalls else 0.0,
        "macro_f05": float(np.mean(f05_scores)) if f05_scores else 0.0,
    }


class Evaluator:
    """Evaluator class wrapping competition metric calculations."""

    def evaluate(
        self,
        ground_truth_df: pd.DataFrame,
        predictions_df: pd.DataFrame,
    ) -> Dict[str, float]:
        """Run complete metric evaluation.

        Args:
            ground_truth_df: Ground truth DataFrame.
            predictions_df: Predictions DataFrame.

        Returns:
            Dictionary of macro-averaged metrics.
        """
        return calculate_macro_f05(ground_truth_df, predictions_df)
