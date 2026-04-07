"""
test_project.py - Comprehensive error and bug check for the entire project.

Tests all modules: utils, preprocessing, training, prediction, and app imports.
Uses ASCII-only output to avoid Windows cp1252 encoding issues.
"""

import sys
import os
import traceback

# Force UTF-8 output on Windows
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

errors = []
warnings_list = []
passed = []


def test_section(name, func):
    """Run a test and track result."""
    try:
        func()
        passed.append(name)
        print("  [PASS] " + name)
    except Exception as e:
        errors.append((name, str(e), traceback.format_exc()))
        print("  [FAIL] " + name)
        print("         " + str(e))


# ============================================================
# TEST 1: Module Imports
# ============================================================
print("\n" + "=" * 60)
print("TEST 1: Module Imports")
print("=" * 60)


def test_utils_import():
    from src.utils import (
        classify_performance, get_confidence_level,
        format_metric, validate_input, save_prediction_history,
        load_prediction_history, generate_sample_dataset,
    )


def test_preprocessing_import():
    from src.preprocessing import DataPreprocessor


def test_train_import():
    from src.train import ModelTrainer


def test_predict_import():
    from src.predict import StudentPredictor


def test_streamlit_import():
    import streamlit


def test_sklearn_import():
    from sklearn.linear_model import LinearRegression
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.model_selection import train_test_split


def test_viz_import():
    import matplotlib.pyplot as plt
    import seaborn as sns


test_section("Import src.utils", test_utils_import)
test_section("Import src.preprocessing", test_preprocessing_import)
test_section("Import src.train", test_train_import)
test_section("Import src.predict", test_predict_import)
test_section("Import streamlit", test_streamlit_import)
test_section("Import sklearn", test_sklearn_import)
test_section("Import matplotlib/seaborn", test_viz_import)


# ============================================================
# TEST 2: Utils Functions
# ============================================================
print("\n" + "=" * 60)
print("TEST 2: Utility Functions")
print("=" * 60)


def test_classify_performance():
    from src.utils import classify_performance
    assert "Excellent" in classify_performance(90)[0]
    assert "High" in classify_performance(75)[0]
    assert "Medium" in classify_performance(55)[0]
    assert "Low" in classify_performance(40)[0]
    assert "Very Low" in classify_performance(20)[0]


def test_get_confidence():
    from src.utils import get_confidence_level
    pct, label, color = get_confidence_level(0.95, 75)
    assert pct > 0
    assert isinstance(label, str)


def test_validate_input():
    from src.utils import validate_input
    valid, msg = validate_input(5, 80, 70)
    assert valid is True, f"Expected valid=True but got: {msg}"
    invalid, msg = validate_input(25, 80, 70)  # Hours > 24
    assert invalid is False, "Expected invalid=False for hours=25"


def test_format_metric():
    from src.utils import format_metric
    assert format_metric(3.14159, 2) == 3.14
    assert format_metric(3.14159, 4) == 3.1416


test_section("classify_performance()", test_classify_performance)
test_section("get_confidence_level()", test_get_confidence)
test_section("validate_input()", test_validate_input)
test_section("format_metric()", test_format_metric)


# ============================================================
# TEST 3: Generate Sample Dataset
# ============================================================
print("\n" + "=" * 60)
print("TEST 3: Sample Data Generation")
print("=" * 60)


def test_generate_dataset():
    from src.utils import generate_sample_dataset
    import pandas as pd

    df = generate_sample_dataset(n_samples=100, save_path="data/student_data.csv")
    assert isinstance(df, pd.DataFrame), "Result must be a DataFrame"
    assert len(df) == 100, f"Expected 100 rows, got {len(df)}"
    for col in ["study_hours", "attendance", "previous_marks", "marks", "participation"]:
        assert col in df.columns, f"Missing column: {col}"
    assert df["marks"].min() >= 0, "Marks below 0 found"
    assert df["marks"].max() <= 100, "Marks above 100 found"
    assert os.path.exists("data/student_data.csv"), "CSV file not saved"


test_section("generate_sample_dataset()", test_generate_dataset)


# ============================================================
# TEST 4: Data Preprocessing
# ============================================================
print("\n" + "=" * 60)
print("TEST 4: Data Preprocessing")
print("=" * 60)


def test_load_data():
    from src.preprocessing import DataPreprocessor
    pp = DataPreprocessor()
    df = pp.load_data("data/student_data.csv")
    assert len(df) == 100


def test_validate_dataset():
    from src.preprocessing import DataPreprocessor
    import pandas as pd
    pp = DataPreprocessor()
    df = pd.read_csv("data/student_data.csv")
    valid, msg = pp.validate_dataset(df)
    assert valid is True, f"Dataset invalid: {msg}"


def test_handle_missing():
    from src.preprocessing import DataPreprocessor
    import pandas as pd
    import numpy as np
    pp = DataPreprocessor()
    df = pd.read_csv("data/student_data.csv")
    df.loc[0, "study_hours"] = np.nan  # Inject missing value
    df_clean = pp.handle_missing_values(df)
    assert df_clean.isnull().sum().sum() == 0, "Missing values remain after handling"


def test_full_preprocess():
    from src.preprocessing import DataPreprocessor
    import pandas as pd
    pp = DataPreprocessor()
    df = pd.read_csv("data/student_data.csv")
    X, y, features = pp.preprocess(df, fit=True)
    assert X.shape[0] == 100
    assert X.shape[1] > 0
    assert len(y) == 100
    assert pp.is_fitted is True


def test_prepare_single_input():
    from src.preprocessing import DataPreprocessor
    import pandas as pd
    pp = DataPreprocessor()
    df = pd.read_csv("data/student_data.csv")
    pp.preprocess(df, fit=True)
    X = pp.prepare_single_input({
        "study_hours": 5.0,
        "attendance": 80.0,
        "previous_marks": 65.0,
        "participation": "High",
    })
    assert X.shape == (1, len(pp.feature_columns)), (
        f"Expected shape (1, {len(pp.feature_columns)}), got {X.shape}"
    )


test_section("load_data()", test_load_data)
test_section("validate_dataset()", test_validate_dataset)
test_section("handle_missing_values()", test_handle_missing)
test_section("full preprocess pipeline", test_full_preprocess)
test_section("prepare_single_input()", test_prepare_single_input)


# ============================================================
# TEST 5: Model Training
# ============================================================
print("\n" + "=" * 60)
print("TEST 5: Model Training")
print("=" * 60)


def test_full_training():
    from src.train import ModelTrainer

    trainer = ModelTrainer(model_dir="models")
    results = trainer.full_training_pipeline("data/student_data.csv")

    assert "results" in results
    assert "best_model" in results
    assert results["best_model"] in [
        "Linear Regression", "Decision Tree", "Random Forest"
    ], f"Unexpected best_model: {results['best_model']}"

    for model_name, res in results["results"].items():
        assert "mae" in res, f"{model_name} missing 'mae'"
        assert "rmse" in res, f"{model_name} missing 'rmse'"
        assert "r2_score" in res, f"{model_name} missing 'r2_score'"
        assert res["r2_score"] > 0, (
            f"{model_name} has non-positive R2: {res['r2_score']}"
        )

    assert os.path.exists("models/best_model.joblib")
    assert os.path.exists("models/preprocessor.joblib")
    assert os.path.exists("models/model_metadata.json")


test_section("full_training_pipeline()", test_full_training)


# ============================================================
# TEST 6: Prediction
# ============================================================
print("\n" + "=" * 60)
print("TEST 6: Prediction")
print("=" * 60)


def test_load_model():
    from src.predict import StudentPredictor
    predictor = StudentPredictor(model_dir="models")
    success = predictor.load_model()
    assert success is True, "load_model() returned False"
    assert predictor.is_loaded is True


def test_predict_basic():
    from src.predict import StudentPredictor
    predictor = StudentPredictor(model_dir="models")
    predictor.load_model()
    result = predictor.predict({
        "study_hours": 6.0,
        "attendance": 85.0,
        "previous_marks": 72.0,
        "participation": "High",
    })
    assert isinstance(result, float), f"Expected float, got {type(result)}"
    assert 0 <= result <= 100, f"Prediction out of range: {result}"


def test_predict_edge_cases():
    from src.predict import StudentPredictor
    predictor = StudentPredictor(model_dir="models")
    predictor.load_model()

    result_low = predictor.predict({
        "study_hours": 0.0,
        "attendance": 30.0,
        "previous_marks": 20.0,
        "participation": "Low",
    })
    assert 0 <= result_low <= 100

    result_high = predictor.predict({
        "study_hours": 12.0,
        "attendance": 100.0,
        "previous_marks": 100.0,
        "participation": "High",
    })
    assert 0 <= result_high <= 100
    assert result_high > result_low, (
        f"High inputs ({result_high}) should yield more than low inputs ({result_low})"
    )


def test_model_info():
    from src.predict import StudentPredictor
    predictor = StudentPredictor(model_dir="models")
    predictor.load_model()
    info = predictor.get_model_info()
    assert "best_model" in info
    assert "metrics" in info


test_section("load_model()", test_load_model)
test_section("predict() basic", test_predict_basic)
test_section("predict() edge cases", test_predict_edge_cases)
test_section("get_model_info()", test_model_info)


# ============================================================
# TEST 7: Prediction History
# ============================================================
print("\n" + "=" * 60)
print("TEST 7: Prediction History")
print("=" * 60)


def test_save_history():
    from src.utils import save_prediction_history, load_prediction_history

    hist_file = "data/prediction_history.json"
    if os.path.exists(hist_file):
        os.remove(hist_file)

    save_prediction_history({
        "study_hours": 5.0,
        "predicted_marks": 72.5,
        "category": "High",
    }, history_file=hist_file)

    history = load_prediction_history(hist_file)
    assert len(history) == 1, f"Expected 1 record, got {len(history)}"
    assert history[0]["predicted_marks"] == 72.5


test_section("prediction history save/load", test_save_history)


# ============================================================
# TEST 8: Visualization (headless, no display needed)
# ============================================================
print("\n" + "=" * 60)
print("TEST 8: Visualization Functions")
print("=" * 60)


def test_visualizations():
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend for testing
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np

    df = pd.read_csv("data/student_data.csv")
    numeric_df = df.select_dtypes(include=[np.number])

    # Correlation heatmap
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.heatmap(numeric_df.corr(), annot=True, ax=ax1)
    plt.close(fig1)

    # Histogram
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.histplot(df["marks"], kde=True, ax=ax2)
    plt.close(fig2)

    # Bar chart
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    ax3.bar(["Linear", "Tree", "Forest"], [0.85, 0.87, 0.91])
    plt.close(fig3)


test_section("visualization creation (headless)", test_visualizations)


# ============================================================
# TEST 9: App.py Syntax Check (without running Streamlit)
# ============================================================
print("\n" + "=" * 60)
print("TEST 9: app.py Syntax Check")
print("=" * 60)


def test_app_syntax():
    import ast
    with open("app.py", "r", encoding="utf-8") as f:
        source = f.read()
    # Will raise SyntaxError if invalid
    tree = ast.parse(source)
    assert tree is not None, "AST parsing returned None"


test_section("app.py syntax check", test_app_syntax)


# ============================================================
# SUMMARY
# ============================================================
total = len(passed) + len(errors)

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"  Passed  : {len(passed)} / {total}")
print(f"  Failed  : {len(errors)} / {total}")

if errors:
    print("\nFAILED TESTS:")
    for name, err, tb in errors:
        print(f"\n  --- {name} ---")
        print(f"  Error: {err}")
        # Print compact traceback (last 3 lines)
        tb_lines = tb.strip().splitlines()
        for line in tb_lines[-5:]:
            print("  " + line)
else:
    print("\nALL TESTS PASSED! Project is error-free and ready to run.")

print("\n" + "=" * 60)

# Exit with non-zero code if there are failures
sys.exit(1 if errors else 0)
