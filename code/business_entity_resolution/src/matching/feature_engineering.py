"""Feature engineering module for entity pair comparison.

Extracts similarity and distance features for candidate pairs generated during
the blocking stage. Features quantify entity similarity across name, address,
and country fields.
"""

from typing import Dict, List, Tuple
import pandas as pd
import numpy as np


class FeatureExtractor:
    """Extracts pairwise feature vectors for entity matching candidates."""

    def __init__(self):
        """Initialize FeatureExtractor."""
        pass

    def extract_pair_features(self, record1: Dict[str, str], record2: Dict[str, str]) -> Dict[str, float]:
        """Extract similarity feature dictionary for a single pair of records.

        Feature families to engineer:
        1. Business Name Similarity:
           - Exact match indicator
           - Normalized edit distance / Levenshtein similarity
           - Jaro-Winkler similarity
           - Character n-gram Jaccard similarity
           - Token set / token sort similarity
           - TF-IDF cosine similarity
        2. Business Address Similarity:
           - Exact address match indicator
           - Address token overlap ratio
           - Street number / postal code exact match indicators
        3. Country Field Compatibility:
           - Country exact match indicator (open-set string handling)
           - Missing country flag
        4. Record Length & Token Count Ratios

        Args:
            record1: Dict representing Source 1 business entity.
            record2: Dict representing Candidate (Source 2 or 3) entity.

        Returns:
            Dictionary mapping feature names to numerical scalar values.
        """
        name1 = record1.get("business_name", "")
        name2 = record2.get("business_name", "")

        addr1 = record1.get("business_address", "")
        addr2 = record2.get("business_address", "")

        country1 = record1.get("country", "")
        country2 = record2.get("country", "")

        # Skeleton placeholder features
        features = {
            "name_exact_match": float(name1.lower() == name2.lower() and len(name1) > 0),
            "address_exact_match": float(addr1.lower() == addr2.lower() and len(addr1) > 0),
            "country_match": float(country1.lower() == country2.lower() and len(country1) > 0),
        }

        return features

    def extract_candidate_features(
        self,
        candidate_pairs_df: pd.DataFrame,
        source1_df: pd.DataFrame,
        candidate_source_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Extract feature matrix for all candidate pairs in candidate_pairs_df.

        Args:
            candidate_pairs_df: DataFrame containing source1_entity_id and candidate_entity_ids.
            source1_df: DataFrame of Source 1 entities.
            candidate_source_df: Combined DataFrame of Source 2 & Source 3 entities.

        Returns:
            DataFrame where each row corresponds to a (source1_id, candidate_id) pair with feature columns.
        """
        # Placeholder skeleton structure for feature extraction
        feature_rows = []

        # Indexing records by entity_id for fast lookup
        s1_records = source1_df.set_index("entity_id").to_dict("index") if "entity_id" in source1_df.columns else {}
        cand_records = candidate_source_df.set_index("entity_id").to_dict("index") if "entity_id" in candidate_source_df.columns else {}

        for _, row in candidate_pairs_df.iterrows():
            s1_id = row.get("source1_entity_id", "")
            cand_ids_str = row.get("candidate_entity_ids", "")

            cand_ids = [cid.strip() for cid in cand_ids_str.split(",") if cid.strip()]
            s1_rec = s1_records.get(s1_id, {})

            for cand_id in cand_ids:
                cand_rec = cand_records.get(cand_id, {})
                feats = self.extract_pair_features(s1_rec, cand_rec)
                feats["source1_entity_id"] = s1_id
                feats["candidate_entity_id"] = cand_id
                feature_rows.append(feats)

        if not feature_rows:
            return pd.DataFrame(columns=["source1_entity_id", "candidate_entity_id"])

        return pd.DataFrame(feature_rows)
