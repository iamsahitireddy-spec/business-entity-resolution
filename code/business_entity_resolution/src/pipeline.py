"""Main execution pipeline for the Business Entity Resolution Challenge.

Orchestrates the complete lifecycle:
Data Loading -> Preprocessing -> Blocking (Candidate Generation) -> Feature Engineering -> Model Training -> Inference -> Metric Evaluation -> Output Export.
"""

import sys
from pathlib import Path

# Ensure src directory is on path for relative imports if executed directly
current_file = Path(__file__).resolve()
src_dir = current_file.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from src.config import config
from src.data_loader import DataLoader
from src.preprocessing.text_normalization import BusinessNameNormalizer
from src.preprocessing.address_normalization import AddressNormalizer
from src.blocking.candidate_generation import CandidateGenerator
from src.matching.feature_engineering import FeatureExtractor
from src.matching.model import EntityMatchingModel
from src.matching.inference import MatchPredictor
from src.evaluation.evaluate import Evaluator


class EntityResolutionPipeline:
    """Orchestrator class managing end-to-end execution of the entity resolution pipeline."""

    def __init__(self):
        """Initialize pipeline modules."""
        self.data_loader = DataLoader()
        self.name_normalizer = BusinessNameNormalizer()
        self.address_normalizer = AddressNormalizer()
        self.candidate_generator = CandidateGenerator()
        self.feature_extractor = FeatureExtractor()
        self.matching_model = EntityMatchingModel()
        self.predictor = MatchPredictor()
        self.evaluator = Evaluator()

    def run_training_pipeline(self):
        """Run training, cross-validation, and metric evaluation flow."""
        print("=== Step 1: Loading Training Data ===")
        # Note: TSV data will be loaded when available in dataset/train/
        # s1_df, s2_df, s3_df = self.data_loader.load_all_sources(split="train")
        # gt_df = self.data_loader.load_ground_truth()

        print("=== Step 2: Preprocessing & Normalization ===")
        # Apply text and address normalizers

        print("=== Step 3: Blocking / Candidate Generation ===")
        # Generate candidate pairs and save to output/candidate_pairs.tsv

        print("=== Step 4: Feature Engineering ===")
        # Extract similarity features for candidates

        print("=== Step 5: Model Training & Validation ===")
        # Fit ML classifier model on training candidate pairs

        print("=== Step 6: Evaluation ===")
        # Compute Macro F0.5 metric

        print("Pipeline skeleton setup complete.")

    def run_inference_pipeline(self, split: str = "test"):
        """Run candidate generation and matching inference on test set.

        Args:
            split: Target split ('test' or 'train').
        """
        print(f"=== Running Inference on '{split}' Split ===")
        # 1. Load test data
        # 2. Preprocess text & address
        # 3. Generate candidate pairs & export output/candidate_pairs.tsv
        # 4. Extract features
        # 5. Predict match scores using trained matching_model
        # 6. Generate & export output/matching_results.tsv
        pass


def main():
    """Main entry point for running the pipeline."""
    pipeline = EntityResolutionPipeline()
    pipeline.run_training_pipeline()


if __name__ == "__main__":
    main()
