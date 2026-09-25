"""Matching package containing feature engineering, ML matching models, and inference.
"""

from src.matching.feature_engineering import FeatureExtractor
from src.matching.model import EntityMatchingModel
from src.matching.inference import MatchPredictor

__all__ = ["FeatureExtractor", "EntityMatchingModel", "MatchPredictor"]
