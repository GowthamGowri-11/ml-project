"""
train_new_dataset.py - Train models using the new Student Performance dataset.

Dataset columns:
  StudentID, Age, Gender, Ethnicity, ParentalEducation, StudyTimeWeekly,
  Absences, Tutoring, ParentalSupport, Extracurricular, Sports, Music,
  Volunteering, GPA, GradeClass

Target: GPA (continuous regression)  /  GradeClass (classification)

We train THREE regressors to predict GPA:
  - Linear Regression
  - Decision Tree Regressor
  - Random Forest Regressor

The best model (by R²) is saved to models/ alongside the preprocessor and
metadata so the existing Streamlit app can also load it.
"""

import os
import sys
import json
import joblib
import warnings
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "Student_performance_data _.csv")
MODEL_DIR    = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)


# ── Minimal Preprocessor (module-level so joblib can pickle it) ───────────────
class MinimalPreprocessor:
    """
    Lightweight preprocessor wrapper that stores the scaler and feature names
    in a format compatible with the existing app.py.
    """
    def __init__(self, feature_cols, scaler):
        self.feature_columns     = feature_cols
        self.scaler              = scaler
        self.label_encoders      = {}
        self.categorical_columns = []
        self.numerical_columns   = feature_cols
        self.target_column       = "GPA"
        self.is_fitted           = True


# ── 1. Load data ──────────────────────────────────────────────────────────────
def load_data(path):
    print(f"\n{'='*60}")
    print("LOADING DATASET")
    print(f"{'='*60}")
    df = pd.read_csv(path)
    print(f"  Rows   : {df.shape[0]}")
    print(f"  Columns: {df.shape[1]}")
    print(f"  Columns: {list(df.columns)}")
    return df


# ── 2. Preprocess ─────────────────────────────────────────────────────────────
def preprocess(df):
    print(f"\n{'='*60}")
    print("PREPROCESSING")
    print(f"{'='*60}")

    # Drop StudentID — not a feature
    if "StudentID" in df.columns:
        df = df.drop(columns=["StudentID"])

    # Target: GPA (continuous)
    target = "GPA"

    # Handle missing values
    missing = df.isnull().sum().sum()
    print(f"  Missing values: {missing}")
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if df[col].dtype in ["float64", "int64"]:
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna(df[col].mode()[0])

    # Feature columns (all remaining except target & GradeClass)
    drop_cols = [target]
    if "GradeClass" in df.columns:
        drop_cols.append("GradeClass")

    feature_cols = [c for c in df.columns if c not in drop_cols]

    X = df[feature_cols].copy()
    y = df[target].copy()

    print(f"  Feature columns ({len(feature_cols)}): {feature_cols}")
    print(f"  Target column  : {target}")
    print(f"  Target range   : {y.min():.2f} → {y.max():.2f}")

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, feature_cols, scaler


# ── 3. Train & evaluate ───────────────────────────────────────────────────────
def train_and_evaluate(X_train, X_test, y_train, y_test):
    print(f"\n{'='*60}")
    print("TRAINING MODELS")
    print(f"{'='*60}")

    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=42, max_depth=10),
        "Random Forest": RandomForestRegressor(
            n_estimators=100, random_state=42, max_depth=15, n_jobs=-1
        ),
    }

    results = {}
    for name, model in models.items():
        print(f"\n  Training: {name} ...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae  = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2   = r2_score(y_test, y_pred)

        results[name] = {
            "model"      : model,
            "mae"        : round(mae, 4),
            "rmse"       : round(rmse, 4),
            "r2_score"   : round(r2, 4),
            "predictions": y_pred,
        }
        print(f"    MAE  = {mae:.4f}")
        print(f"    RMSE = {rmse:.4f}")
        print(f"    R²   = {r2:.4f}")

    return results


# ── 4. Pick best model ────────────────────────────────────────────────────────
def select_best(results):
    best_name = max(results, key=lambda k: results[k]["r2_score"])
    best      = results[best_name]
    print(f"\n{'='*60}")
    print(f"  BEST MODEL : {best_name}")
    print(f"  R²         : {best['r2_score']}")
    print(f"  MAE        : {best['mae']}")
    print(f"  RMSE       : {best['rmse']}")
    print(f"{'='*60}")
    return best_name, best["model"]


# ── 5. Save artefacts ─────────────────────────────────────────────────────────
def save_artefacts(best_name, best_model, scaler, feature_cols, results):
    print(f"\n{'='*60}")
    print("SAVING ARTEFACTS")
    print(f"{'='*60}")

    # --- model ---
    model_path = os.path.join(MODEL_DIR, "best_model.joblib")
    joblib.dump(best_model, model_path)
    print(f"  Model saved      → {model_path}")

    # --- build a minimal preprocessor-like object so app.py can load it ---
    prep = MinimalPreprocessor(feature_cols, scaler)

    preprocessor_path = os.path.join(MODEL_DIR, "preprocessor.joblib")
    joblib.dump(prep, preprocessor_path)
    print(f"  Preprocessor saved → {preprocessor_path}")

    # --- metadata ---
    metadata = {
        "best_model"     : best_name,
        "target"         : "GPA",
        "dataset"        : "Student_performance_data _.csv",
        "feature_columns": feature_cols,
        "metrics": {
            name: {
                "mae"     : res["mae"],
                "rmse"    : res["rmse"],
                "r2_score": res["r2_score"],
            }
            for name, res in results.items()
        },
    }
    metadata_path = os.path.join(MODEL_DIR, "model_metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"  Metadata saved   → {metadata_path}")

    return model_path


# ── 6. Feature importance ────────────────────────────────────────────────────
def print_feature_importance(model, feature_cols):
    if hasattr(model, "feature_importances_"):
        imp = model.feature_importances_
        pairs = sorted(zip(feature_cols, imp), key=lambda x: -x[1])
        print(f"\n{'='*60}")
        print("FEATURE IMPORTANCE")
        print(f"{'='*60}")
        for feat, score in pairs:
            bar = "█" * int(score * 40)
            print(f"  {feat:<22} {bar} {score:.4f}")
    elif hasattr(model, "coef_"):
        coef = np.abs(model.coef_)
        pairs = sorted(zip(feature_cols, coef), key=lambda x: -x[1])
        print(f"\n{'='*60}")
        print("FEATURE COEFFICIENTS (absolute)")
        print(f"{'='*60}")
        for feat, score in pairs:
            bar = "█" * int(score * 10)
            print(f"  {feat:<22} {bar} {score:.4f}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("\n" + "★" * 60)
    print("  STUDENT PERFORMANCE PREDICTOR — MODEL TRAINING")
    print("  Dataset: Student_performance_data _.csv")
    print("★" * 60)

    # 1. Load
    df = load_data(DATASET_PATH)

    # 2. Preprocess
    X, y, feature_cols, scaler = preprocess(df)

    # 3. Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"\n  Train: {X_train.shape[0]} rows | Test: {X_test.shape[0]} rows")

    # 4. Train
    results = train_and_evaluate(X_train, X_test, y_train, y_test)

    # 5. Best model
    best_name, best_model = select_best(results)

    # 6. Feature importance
    print_feature_importance(best_model, feature_cols)

    # 7. Save
    save_artefacts(best_name, best_model, scaler, feature_cols, results)

    print("\n" + "★" * 60)
    print("  TRAINING COMPLETE ✔")
    print("  Models saved in →  models/")
    print("★" * 60 + "\n")


if __name__ == "__main__":
    main()
