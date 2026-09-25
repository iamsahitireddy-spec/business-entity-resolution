"""Machine Learning Entity Matching Model wrapper.

Encapsulates binary classification algorithms (e.g., Logistic Regression,
Gradient Boosted Decision Trees, Random Forests) for scoring candidate record pairs.

Keeps model logic completely isolated from feature extraction and inference.
"""

from pathlib import Path
from typing import Any, Optional, Union
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


class EntityMatchingModel:
    """Classifier model wrapper for scoring pairwise business entity candidates."""

    def __init__(self, model_type: str = "logistic_regression", model_params: Optional[dict] = None):
        """Initialize entity matching model.

        Args:
            model_type: Model architecture identifier (e.g., 'logistic_regression', 'gbdt').
            model_params: Optional dictionary of hyper-parameters.
        """
        self.model_type = model_type
        self.model_params = model_params or {}
        self.model = self._build_model()

    def _build_model(self) -> Any:
        """Construct underlying scikit-learn compatible classifier instance."""
        if self.model_type == "logistic_regression":
            return LogisticRegression(**self.model_params)
        else:
            # Placeholder for alternative classifiers (e.g. LightGBM / XGBoost / Random Forest)
            return LogisticRegression(**self.model_params)

    def fit(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray]) -> "EntityMatchingModel":
        """Train classifier model on pairwise feature matrix X and binary target labels y.

        Args:
            X: Feature matrix of candidate pairs.
            y: Binary target labels (1 = match, 0 = non-match).

        Returns:
            Fitted EntityMatchingModel instance.
        """
        self.model.fit(X, y)
        return self

    def predict_proba(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Predict pair match probabilities.

        Args:
            X: Feature matrix of candidate pairs.

        Returns:
            Numpy array of predicted probability scores for positive match class.
        """
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X)
            # Return positive class probabilities
            return probs[:, 1] if probs.ndim == 2 and probs.shape[1] > 1 else probs
        else:
            return self.model.predict(X).astype(float)

    def predict(self, X: Union[pd.DataFrame, np.ndarray], threshold: float = 0.5) -> np.ndarray:
        """Predict binary match decisions based on a probability decision threshold.

        Args:
            X: Feature matrix of candidate pairs.
            threshold: Match decision probability threshold.

        Returns:
            Binary predictions array (1 for match, 0 for non-match).
        """
        probabilities = self.predict_proba(X)
        return (probabilities >= threshold).astype(int)
