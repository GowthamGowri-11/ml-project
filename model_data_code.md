# Model Data Code Documentation

## Overview

This document contains all the code and documentation for the Student Performance Predictor machine learning models. The system uses three regression models to predict student GPA based on 12 input features.

---

## Model Training Code

### Complete Training Script (`train_new_dataset.py`)

```python
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
```

---

## Dataset Information

### Dataset File
- **Name**: `Student_performance_data _.csv`
- **Location**: `dataset/` folder
- **Total Records**: 2,410 students
- **Total Features**: 15 columns

### Dataset Columns

| Column Name | Type | Description |
|------------|------|-------------|
| StudentID | Integer | Unique identifier for each student |
| Age | Integer | Student's age (15-18) |
| Gender | Binary | 0 = Female, 1 = Male |
| Ethnicity | Categorical | Student's ethnic background |
| ParentalEducation | Ordinal | 0-4 (None to Higher Education) |
| StudyTimeWeekly | Float | Hours spent studying per week |
| Absences | Integer | Number of absences |
| Tutoring | Binary | 0 = No, 1 = Yes |
| ParentalSupport | Integer | Level of parental support (0-4) |
| Extracurricular | Binary | Participation in activities |
| Sports | Binary | Participation in sports |
| Music | Binary | Participation in music |
| Volunteering | Binary | Participation in volunteering |
| GPA | Float | Grade Point Average (0-10 scale) - TARGET |
| GradeClass | Integer | Grade classification (0-4: A-F) |

---

## Machine Learning Models

### 1. Linear Regression
```python
LinearRegression()
```
- **Accuracy**: 95.32%
- **R² Score**: 0.9532
- **MAE**: 0.1553
- **RMSE**: 0.1966
- **Status**: BEST MODEL (Currently Used)

**Advantages**:
- Highest accuracy among all models
- Fast training and prediction
- Low computational requirements
- Excellent for linear relationships

**Use Case**: Primary model for production predictions

---

### 2. Decision Tree Regressor
```python
DecisionTreeRegressor(random_state=42, max_depth=10)
```
- **Accuracy**: 87.08%
- **R² Score**: 0.8708
- **MAE**: 0.2891
- **RMSE**: 0.3267

**Advantages**:
- Easy to interpret and visualize
- No data preprocessing required
- Handles non-linear relationships
- Visual decision rules

**Use Case**: When interpretability is more important than accuracy

---

### 3. Random Forest Regressor
```python
RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    max_depth=15,
    n_jobs=-1
)
```
- **Accuracy**: 92.69%
- **R² Score**: 0.9269
- **MAE**: 0.2156
- **RMSE**: 0.2455

**Advantages**:
- Balanced performance
- Reduces overfitting
- Handles missing data well
- Robust to outliers

**Use Case**: When you need balanced performance and robustness

---

## Data Preprocessing

### Steps

1. **Load Dataset**
   ```python
   df = pd.read_csv("dataset/Student_performance_data _.csv")
   ```

2. **Remove Non-Features**
   - Drop `StudentID` (not a predictive feature)
   - Drop `GradeClass` (derived from GPA)

3. **Handle Missing Values**
   - Numerical columns: Fill with median
   - Categorical columns: Fill with mode

4. **Feature Scaling**
   ```python
   scaler = StandardScaler()
   X_scaled = scaler.fit_transform(X)
   ```

5. **Train-Test Split**
   - Training: 80% (1,928 records)
   - Testing: 20% (482 records)
   - Random state: 42 (for reproducibility)

---

## Model Evaluation Metrics

### R² Score (Coefficient of Determination)
- Measures how well the model explains variance in GPA
- Range: 0 to 1 (1 = perfect prediction)
- **Linear Regression**: 0.9532 (95.32%)

### MAE (Mean Absolute Error)
- Average absolute difference between predicted and actual GPA
- Lower is better
- **Linear Regression**: 0.1553 (±0.39 GPA points on 10-point scale)

### RMSE (Root Mean Squared Error)
- Penalizes larger errors more heavily
- Lower is better
- **Linear Regression**: 0.1966 (±0.49 GPA points on 10-point scale)

---

## Saved Model Files

### Location: `models/` folder

1. **best_model.joblib**
   - The trained Linear Regression model
   - Used for making predictions

2. **preprocessor.joblib**
   - Contains the StandardScaler
   - Feature column names
   - Preprocessing configuration

3. **model_metadata.json**
   - Model performance metrics
   - Feature information
   - Training configuration

---

## How to Retrain Models

### Command
```bash
python train_new_dataset.py
```

### Output
```
★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
  STUDENT PERFORMANCE PREDICTOR — MODEL TRAINING
  Dataset: Student_performance_data _.csv
★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★

============================================================
LOADING DATASET
============================================================
  Rows   : 2410
  Columns: 15

============================================================
PREPROCESSING
============================================================
  Missing values: 0
  Feature columns (12): ['Age', 'Gender', 'Ethnicity', ...]
  Target column  : GPA
  Target range   : 0.00 → 10.00

  Train: 1928 rows | Test: 482 rows

============================================================
TRAINING MODELS
============================================================

  Training: Linear Regression ...
    MAE  = 0.1553
    RMSE = 0.1966
    R²   = 0.9532

  Training: Decision Tree ...
    MAE  = 0.2891
    RMSE = 0.3267
    R²   = 0.8708

  Training: Random Forest ...
    MAE  = 0.2156
    RMSE = 0.2455
    R²   = 0.9269

============================================================
  BEST MODEL : Linear Regression
  R²         : 0.9532
  MAE        : 0.1553
  RMSE       : 0.1966
============================================================

============================================================
SAVING ARTEFACTS
============================================================
  Model saved      → models/best_model.joblib
  Preprocessor saved → models/preprocessor.joblib
  Metadata saved   → models/model_metadata.json

★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
  TRAINING COMPLETE ✔
  Models saved in →  models/
★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
```

---

## Dependencies

```python
# Core Libraries
import numpy as np
import pandas as pd
import joblib
import json

# Scikit-learn
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
```

### Requirements
```
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
joblib>=1.1.0
```

---

## Feature Importance

Based on Linear Regression coefficients (absolute values):

1. **StudyTimeWeekly** - Most important predictor
2. **Absences** - Strong negative correlation
3. **ParentalSupport** - Significant positive impact
4. **Tutoring** - Moderate positive effect
5. **Age** - Minor influence
6. **Extracurricular Activities** - Small positive effect
7. **Gender, Ethnicity** - Minimal direct impact

---

## Model Update Workflow

1. **Add New Data**
   - Append new records to `dataset/Student_performance_data _.csv`
   - Ensure all 15 columns are present

2. **Retrain Models**
   ```bash
   python train_new_dataset.py
   ```

3. **Verify Performance**
   - Check R² score (should be ≥ 0.90)
   - Check MAE (should be ≤ 0.20)
   - Review feature importance

4. **Deploy**
   - Models automatically saved to `models/` folder
   - Streamlit app will load new models on restart

---

## Notes

- All models use `random_state=42` for reproducibility
- StandardScaler is applied to all features
- Target variable (GPA) is on a 0-10 scale
- Test set is 20% of total data
- Models are saved using joblib for efficient serialization

---

## Troubleshooting

### Issue: Low Model Accuracy
**Solution**: 
- Check for data quality issues
- Increase training data size
- Try different hyperparameters

### Issue: Model File Not Found
**Solution**:
- Run `python train_new_dataset.py` to generate models
- Ensure `models/` folder exists

### Issue: Prediction Errors
**Solution**:
- Verify input features match training data format
- Check for missing or invalid values
- Ensure StandardScaler is applied

---

**Last Updated**: April 10, 2026  
**Version**: 2.0  
**Author**: Student Performance Predictor Team
