"""Structure and import validation tests for the Business Entity Resolution skeleton.
"""

import sys
from pathlib import Path

# Ensure src directory is in path
repo_root = Path(__file__).resolve().parent.parent
src_dir = repo_root / "code" / "business_entity_resolution"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

import pytest
from src.config import config
from src.data_loader import DataLoader, parse_matched_ids
from src.preprocessing.text_normalization import BusinessNameNormalizer
from src.preprocessing.address_normalization import AddressNormalizer
from src.blocking.candidate_generation import CandidateGenerator
from src.matching.feature_engineering import FeatureExtractor
from src.matching.model import EntityMatchingModel
from src.matching.inference import MatchPredictor
from src.evaluation.evaluate import Evaluator, calculate_entity_f05, calculate_macro_f05
from src.pipeline import EntityResolutionPipeline


def test_config_paths():
    """Verify config paths resolution."""
    assert config.REPO_ROOT.exists()
    assert config.DELIMITER == "\t"
    assert config.PREFIX_SOURCE1 == "S1-"


def test_normalizers():
    """Verify text and address normalizers run syntactically."""
    name_norm = BusinessNameNormalizer()
    assert name_norm.normalize("Acme Corp.") == "acme corporation"

    addr_norm = AddressNormalizer()
    assert addr_norm.normalize("123 Main St.") == "123 main street"


def test_f05_evaluation_metric():
    """Verify macro F0.5 metric calculation logic."""
    # Singleton correctly predicted -> 1.0
    p, r, f05 = calculate_entity_f05(set(), set())
    assert f05 == 1.0

    # Singleton false merge -> 0.0
    p, r, f05 = calculate_entity_f05(set(), {"S2-100"})
    assert f05 == 0.0

    # Match exact -> 1.0
    p, r, f05 = calculate_entity_f05({"S2-100", "S3-200"}, {"S2-100", "S3-200"})
    assert f05 == 1.0


def test_pipeline_instantiation():
    """Verify pipeline class can be instantiated without errors."""
    pipeline = EntityResolutionPipeline()
    assert pipeline is not None
