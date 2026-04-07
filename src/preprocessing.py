"""
preprocessing.py - Data cleaning and encoding module.

Handles all data preprocessing tasks including:
- Missing value handling
- Categorical encoding
- Feature scaling
- Feature selection
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import warnings

warnings.filterwarnings("ignore")


class DataPreprocessor:
    """
    Handles data preprocessing for the student performance dataset.

    This class provides methods to clean, encode, and prepare data
    for model training and prediction.
    """

    def __init__(self):
        """Initialize the preprocessor with empty encoders and scaler."""
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.target_column = "marks"
        self.categorical_columns = []
        self.numerical_columns = []
        self.is_fitted = False

    def load_data(self, filepath):
        """
        Load dataset from a CSV file.

        Args:
            filepath (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Loaded DataFrame.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If required columns are missing.
        """
        try:
            df = pd.read_csv(filepath)
            print(f"[OK] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"[ERROR] Dataset not found at: {filepath}")
        except Exception as e:
            raise ValueError(f"[ERROR] Error loading dataset: {str(e)}")

    def validate_dataset(self, df):
        """
        Validate that the dataset has the minimum required columns.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            tuple: (is_valid, message)
        """
        required_columns = ["study_hours", "attendance", "previous_marks", "marks"]
        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            return False, f"Missing required columns: {', '.join(missing)}"

        if df.empty:
            return False, "Dataset is empty."

        if len(df) < 10:
            return False, "Dataset too small. Need at least 10 records."

        return True, "Dataset is valid [OK]"

    def handle_missing_values(self, df):
        """
        Handle missing values in the dataset.

        Strategy:
        - Numerical columns: Fill with median
        - Categorical columns: Fill with mode

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: DataFrame with missing values handled.
        """
        df = df.copy()
        missing_before = df.isnull().sum().sum()

        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype in ["float64", "int64", "float32", "int32"]:
                    # Fill numerical with median (assignment avoids inplace deprecation)
                    df[col] = df[col].fillna(df[col].median())
                else:
                    # Fill categorical with mode
                    mode_val = df[col].mode()
                    if len(mode_val) > 0:
                        df[col] = df[col].fillna(mode_val[0])

        missing_after = df.isnull().sum().sum()
        print(f"[INFO] Missing values: {missing_before} -> {missing_after}")

        return df

    def identify_column_types(self, df):
        """
        Identify categorical and numerical columns automatically.

        Args:
            df (pd.DataFrame): Input DataFrame.
        """
        self.categorical_columns = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        self.numerical_columns = df.select_dtypes(
            include=["int64", "float64", "int32", "float32"]
        ).columns.tolist()

        # Remove target from feature lists
        if self.target_column in self.numerical_columns:
            self.numerical_columns.remove(self.target_column)

        print(f"[INFO] Numerical features: {self.numerical_columns}")
        print(f"[INFO] Categorical features: {self.categorical_columns}")

    def encode_categorical(self, df, fit=True):
        """
        Encode categorical variables using LabelEncoder.

        Args:
            df (pd.DataFrame): Input DataFrame.
            fit (bool): Whether to fit the encoders (True for training).

        Returns:
            pd.DataFrame: DataFrame with encoded categorical columns.
        """
        df = df.copy()

        for col in self.categorical_columns:
            if col in df.columns:
                if fit:
                    # Fit and transform
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    # Transform only (for prediction)
                    if col in self.label_encoders:
                        le = self.label_encoders[col]
                        # Handle unseen categories
                        df[col] = df[col].astype(str).apply(
                            lambda x: le.transform([x])[0]
                            if x in le.classes_
                            else -1
                        )

        return df

    def scale_features(self, X, fit=True):
        """
        Scale numerical features using StandardScaler.

        Args:
            X (pd.DataFrame): Feature DataFrame.
            fit (bool): Whether to fit the scaler (True for training).

        Returns:
            np.ndarray: Scaled features.
        """
        if fit:
            return self.scaler.fit_transform(X)
        else:
            return self.scaler.transform(X)

    def preprocess(self, df, fit=True):
        """
        Full preprocessing pipeline.

        Steps:
        1. Handle missing values
        2. Identify column types
        3. Encode categorical variables
        4. Separate features and target
        5. Scale features

        Args:
            df (pd.DataFrame): Input DataFrame.
            fit (bool): Whether to fit transformers (True for training).

        Returns:
            tuple: (X_scaled, y, feature_names)
        """
        # Step 1: Handle missing values
        df = self.handle_missing_values(df)

        # Step 2: Identify column types (only during fitting)
        if fit:
            self.identify_column_types(df)

        # Step 3: Encode categorical variables
        df = self.encode_categorical(df, fit=fit)

        # Step 4: Separate features and target
        feature_cols = [
            col for col in df.columns if col != self.target_column
        ]

        if fit:
            self.feature_columns = feature_cols

        X = df[self.feature_columns]
        y = df[self.target_column] if self.target_column in df.columns else None

        # Step 5: Scale features
        X_scaled = self.scale_features(X, fit=fit)

        if fit:
            self.is_fitted = True

        print(f"[OK] Preprocessing complete. Features shape: {X_scaled.shape}")

        return X_scaled, y, self.feature_columns

    def prepare_single_input(self, input_dict):
        """
        Prepare a single input for prediction.

        Args:
            input_dict (dict): Dictionary with feature values.
                Example: {
                    "study_hours": 6.0,
                    "attendance": 85.0,
                    "previous_marks": 72.0,
                    "participation": "High"
                }

        Returns:
            np.ndarray: Scaled feature array ready for prediction.
        """
        if not self.is_fitted:
            raise ValueError("Preprocessor not fitted. Train a model first.")

        # Create DataFrame from input
        input_df = pd.DataFrame([input_dict])

        # Encode categorical columns
        input_df = self.encode_categorical(input_df, fit=False)

        # Ensure all feature columns are present
        for col in self.feature_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        # Select and order feature columns
        X = input_df[self.feature_columns]

        # Scale features
        X_scaled = self.scale_features(X, fit=False)

        return X_scaled

    def split_data(self, X, y, test_size=0.2, random_state=42):
        """
        Split data into training and testing sets.

        Args:
            X (np.ndarray): Feature array.
            y (pd.Series): Target array.
            test_size (float): Proportion for test set.
            random_state (int): Random seed for reproducibility.

        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        print(f"[INFO] Train set: {X_train.shape[0]} | Test set: {X_test.shape[0]}")
        return X_train, X_test, y_train, y_test
