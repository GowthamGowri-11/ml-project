"""
train.py - Model training module.

Trains and compares multiple regression models:
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

Automatically selects the best performing model based on R² score.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.preprocessing import DataPreprocessor


class ModelTrainer:
    """
    Trains, evaluates, and manages ML models for student performance prediction.
    """

    def __init__(self, model_dir="models"):
        """
        Initialize the trainer.

        Args:
            model_dir (str): Directory to save trained models.
        """
        self.model_dir = model_dir
        self.models = {}
        self.results = {}
        self.best_model_name = None
        self.best_model = None
        self.preprocessor = DataPreprocessor()

        # Ensure model directory exists
        os.makedirs(self.model_dir, exist_ok=True)

    def _get_models(self):
        """
        Get dictionary of models to train.

        Returns:
            dict: Model name → model instance mapping.
        """
        return {
            "Linear Regression": LinearRegression(),
            "Decision Tree": DecisionTreeRegressor(
                random_state=42, max_depth=10
            ),
            "Random Forest": RandomForestRegressor(
                n_estimators=100, random_state=42, max_depth=15, n_jobs=-1
            ),
        }

    def train_and_evaluate(self, X_train, X_test, y_train, y_test):
        """
        Train all models and evaluate their performance.

        Args:
            X_train (np.ndarray): Training features.
            X_test (np.ndarray): Testing features.
            y_train (pd.Series): Training target.
            y_test (pd.Series): Testing target.

        Returns:
            dict: Results for each model with metrics.
        """
        self.models = self._get_models()
        self.results = {}

        print("\n" + "=" * 60)
        print("TRAINING MODELS")
        print("=" * 60)

        for name, model in self.models.items():
            print(f"\n[INFO] Training: {name}...")

            # Train the model
            model.fit(X_train, y_train)

            # Make predictions
            y_pred = model.predict(X_test)

            # Calculate metrics
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)

            # Store results
            self.results[name] = {
                "model": model,
                "mae": round(mae, 4),
                "rmse": round(rmse, 4),
                "r2_score": round(r2, 4),
                "predictions": y_pred,
            }

            print(f"   MAE:  {mae:.4f}")
            print(f"   RMSE: {rmse:.4f}")
            print(f"   R2:   {r2:.4f}")

        # Select best model
        self._select_best_model()

        return self.results

    def _select_best_model(self):
        """Select the best model based on highest R² score."""
        best_name = max(
            self.results, key=lambda k: self.results[k]["r2_score"]
        )
        self.best_model_name = best_name
        self.best_model = self.results[best_name]["model"]

        print(f"\n[BEST] Best Model: {best_name}")
        print(f"   R2 Score: {self.results[best_name]['r2_score']}")

    def save_model(self, preprocessor=None):
        """
        Save the best model and preprocessor to disk.

        Args:
            preprocessor (DataPreprocessor): The fitted preprocessor.

        Returns:
            str: Path to the saved model file.
        """
        if self.best_model is None:
            raise ValueError("No model trained yet. Run train_and_evaluate first.")

        # Save the model
        model_path = os.path.join(self.model_dir, "best_model.joblib")
        joblib.dump(self.best_model, model_path)
        print(f"[SAVED] Model saved: {model_path}")

        # Save the preprocessor
        if preprocessor is not None:
            preprocessor_path = os.path.join(self.model_dir, "preprocessor.joblib")
            joblib.dump(preprocessor, preprocessor_path)
            print(f"[SAVED] Preprocessor saved: {preprocessor_path}")

        # Save model metadata
        metadata = {
            "best_model": self.best_model_name,
            "metrics": {
                name: {
                    "mae": res["mae"],
                    "rmse": res["rmse"],
                    "r2_score": res["r2_score"],
                }
                for name, res in self.results.items()
            },
            "feature_columns": (
                preprocessor.feature_columns if preprocessor else []
            ),
        }

        metadata_path = os.path.join(self.model_dir, "model_metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        print(f"[SAVED] Metadata saved: {metadata_path}")

        return model_path

    def get_feature_importance(self):
        """
        Get feature importance from the best model (if available).

        Returns:
            dict or None: Feature name → importance mapping.
        """
        if self.best_model is None:
            return None

        # Check if model has feature_importances_ attribute
        if hasattr(self.best_model, "feature_importances_"):
            importance = self.best_model.feature_importances_
            feature_names = self.preprocessor.feature_columns
            if len(feature_names) == len(importance):
                return dict(zip(feature_names, importance))

        # For Linear Regression, use coefficients
        if hasattr(self.best_model, "coef_"):
            coefficients = np.abs(self.best_model.coef_)
            feature_names = self.preprocessor.feature_columns
            if len(feature_names) == len(coefficients):
                return dict(zip(feature_names, coefficients))

        return None

    def full_training_pipeline(self, data_path):
        """
        Run the complete training pipeline.

        Steps:
        1. Load data
        2. Preprocess data
        3. Split data
        4. Train and evaluate models
        5. Save best model

        Args:
            data_path (str): Path to the CSV dataset.

        Returns:
            dict: Training results and metadata.
        """
        print("Starting full training pipeline...\n")

        # Step 1: Load data
        df = self.preprocessor.load_data(data_path)

        # Validate dataset
        is_valid, message = self.preprocessor.validate_dataset(df)
        if not is_valid:
            raise ValueError(message)
        print(f"   [OK] {message}")

        # Step 2: Preprocess
        X, y, feature_names = self.preprocessor.preprocess(df, fit=True)

        # Step 3: Split
        X_train, X_test, y_train, y_test = self.preprocessor.split_data(X, y)

        # Step 4: Train and evaluate
        results = self.train_and_evaluate(X_train, X_test, y_train, y_test)

        # Step 5: Save best model
        self.save_model(preprocessor=self.preprocessor)

        return {
            "results": results,
            "best_model": self.best_model_name,
            "feature_names": feature_names,
            "preprocessor": self.preprocessor,
            "y_test": y_test,
            "y_pred": results[self.best_model_name]["predictions"],
        }
