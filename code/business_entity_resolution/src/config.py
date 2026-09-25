"""Configuration settings for the Business Entity Resolution pipeline.

Centralizes paths, filenames, entity prefix definitions, threshold settings,
and pipeline hyper-parameters to avoid hardcoded constants across modules.
"""

from pathlib import Path


class Config:
    """Central configuration class containing directory paths and pipeline parameters."""

    # Dynamic determination of repository root directory
    # Assumes this file is located at <repo_root>/code/business_entity_resolution/src/config.py
    SRC_DIR = Path(__file__).resolve().parent
    PACKAGE_DIR = SRC_DIR.parent
    CODE_DIR = PACKAGE_DIR.parent
    REPO_ROOT = CODE_DIR.parent

    # Dataset Directories
    DATASET_DIR = REPO_ROOT / "dataset"
    TRAIN_DIR = DATASET_DIR / "train"
    TEST_DIR = DATASET_DIR / "test"

    # Output Directory
    OUTPUT_DIR = REPO_ROOT / "output"

    # Expected File Names
    SOURCE1_FILENAME = "source1.tsv"  # e.g., train_source1.tsv or test_source1.tsv
    SOURCE2_FILENAME = "source2.tsv"
    SOURCE3_FILENAME = "source3.tsv"
    GROUND_TRUTH_FILENAME = "train_ground_truth.tsv"

    # Required Submission Output Filenames
    MATCHING_RESULTS_FILENAME = "matching_results.tsv"
    CANDIDATE_PAIRS_FILENAME = "candidate_pairs.tsv"

    # File Delimiter (Tab-Separated Values)
    DELIMITER = "\t"

    # Entity ID Prefixes
    PREFIX_SOURCE1 = "S1-"
    PREFIX_SOURCE2 = "S2-"
    PREFIX_SOURCE3 = "S3-"

    # Standard Dataset Column Names
    COL_ENTITY_ID = "entity_id"
    COL_NAME = "business_name"
    COL_ADDRESS = "business_address"
    COL_COUNTRY = "country"

    # Ground Truth & Output Column Names
    COL_S1_ID = "source1_entity_id"
    COL_MATCHED_IDS = "matched_entity_ids"
    COL_CANDIDATE_IDS = "candidate_entity_ids"

    # Evaluation Settings
    F_BETA = 0.5  # Macro F0.5 evaluation metric (precision-heavy)

    # Note on Country Handling:
    # Country labels are treated as open-set strings (e.g. US, India, France).
    # Do not hardcode country-specific filters or assumptions.


config = Config()
