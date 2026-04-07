"""
predict.py - Prediction module.

Loads trained model and preprocessor to make predictions
on new student data.
"""

import os
import json
import joblib
import numpy as np


class StudentPredictor:
    """
    Makes predictions using a trained model and preprocessor.
    """

    def __init__(self, model_dir="models"):
        """
        Initialize the predictor.

        Args:
            model_dir (str): Directory containing saved models.
        """
        self.model_dir = model_dir
        self.model = None
        self.preprocessor = None
        self.metadata = None
        self.is_loaded = False

    def load_model(self):
        """
        Load the trained model, preprocessor, and metadata from disk.

        Returns:
            bool: True if loaded successfully, False otherwise.
        """
        model_path = os.path.join(self.model_dir, "best_model.joblib")
        preprocessor_path = os.path.join(self.model_dir, "preprocessor.joblib")
        metadata_path = os.path.join(self.model_dir, "model_metadata.json")

        try:
            # Load model
            if not os.path.exists(model_path):
                print(f"[ERROR] Model file not found: {model_path}")
                return False
            self.model = joblib.load(model_path)
            print(f"[OK] Model loaded: {model_path}")

            # Load preprocessor
            if os.path.exists(preprocessor_path):
                self.preprocessor = joblib.load(preprocessor_path)
                print(f"[OK] Preprocessor loaded: {preprocessor_path}")
            else:
                print(f"[WARN] Preprocessor not found: {preprocessor_path}")
                return False

            # Load metadata
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    self.metadata = json.load(f)
                print(f"[OK] Metadata loaded: {metadata_path}")

            self.is_loaded = True
            return True

        except Exception as e:
            print(f"[ERROR] Error loading model: {str(e)}")
            return False

    def predict(self, input_data):
        """
        Make a prediction for a single student.

        Args:
            input_data (dict): Student data dictionary.
                Example: {
                    "study_hours": 6.0,
                    "attendance": 85.0,
                    "previous_marks": 72.0,
                    "participation": "High"
                }

        Returns:
            float: Predicted marks (clipped to 0-100 range).

        Raises:
            ValueError: If model is not loaded.
        """
        if not self.is_loaded:
            raise ValueError(
                "Model not loaded. Call load_model() first."
            )

        try:
            # Prepare input using preprocessor
            X = self.preprocessor.prepare_single_input(input_data)

            # Make prediction
            prediction = self.model.predict(X)[0]

            # Clip to valid range
            prediction = np.clip(prediction, 0, 100)

            return round(float(prediction), 2)

        except Exception as e:
            raise ValueError(f"Prediction error: {str(e)}")

    def get_model_info(self):
        """
        Get information about the loaded model.

        Returns:
            dict: Model metadata and info.
        """
        if self.metadata:
            return {
                "best_model": self.metadata.get("best_model", "Unknown"),
                "metrics": self.metadata.get("metrics", {}),
                "features": self.metadata.get("feature_columns", []),
            }
        return {"best_model": "Unknown", "metrics": {}, "features": []}

    def get_best_r2(self):
        """
        Get the R² score of the best model.

        Returns:
            float: R² score, or 0.0 if not available.
        """
        if self.metadata:
            best_name = self.metadata.get("best_model", "")
            metrics = self.metadata.get("metrics", {})
            if best_name in metrics:
                return metrics[best_name].get("r2_score", 0.0)
        return 0.0
