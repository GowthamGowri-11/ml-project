"""
run_tests.py - Clean test runner that writes results to JSON.
Avoids emoji and multiline shell issues.
"""

import sys
import os
import json
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

results = {}


def run_test(name, func):
    try:
        val = func()
        results[name] = f"PASS" + (f" - {val}" if val else "")
    except Exception as e:
        tb = traceback.format_exc()
        results[name] = f"FAIL: {e}"
        # Store detailed error for later analysis
        results[name + "_tb"] = tb


# ─── TEST 1: Imports ──────────────────────────────────────────
def t_imports():
    from src.utils import classify_performance, validate_input, generate_sample_dataset
    from src.preprocessing import DataPreprocessor
    from src.train import ModelTrainer
    from src.predict import StudentPredictor
    import streamlit
    import sklearn
    import matplotlib
    import seaborn

run_test("1_imports", t_imports)


# ─── TEST 2: Generate Dataset ────────────────────────────────
def t_generate():
    from src.utils import generate_sample_dataset
    df = generate_sample_dataset(150, "data/student_data.csv")
    assert len(df) == 150
    for col in ["study_hours", "attendance", "previous_marks", "marks", "participation"]:
        assert col in df.columns, f"Missing: {col}"
    assert df["marks"].min() >= 0
    assert df["marks"].max() <= 100
    assert os.path.exists("data/student_data.csv")
    return f"150 rows, columns={list(df.columns)}"

run_test("2_generate_dataset", t_generate)


# ─── TEST 3: Utils functions ────────────────────────────────
def t_utils():
    from src.utils import classify_performance, validate_input, format_metric, get_confidence_level

    assert "Excellent" in classify_performance(90)[0]
    assert "High" in classify_performance(75)[0]
    assert "Medium" in classify_performance(55)[0]
    assert "Low" in classify_performance(40)[0]
    assert "Very Low" in classify_performance(20)[0]

    ok, _  = validate_input(5, 75, 60)
    bad, _ = validate_input(25, 75, 60)
    assert ok,  "Should be valid"
    assert not bad, "Should be invalid (hours > 24)"

    assert format_metric(3.14159, 2) == 3.14
    assert format_metric(3.14159, 4) == 3.1416

    pct, lbl, col = get_confidence_level(0.9, 75)
    assert pct > 0

run_test("3_utils_functions", t_utils)


# ─── TEST 4: Preprocessing ───────────────────────────────────
def t_preprocess():
    import pandas as pd
    import numpy as np
    from src.preprocessing import DataPreprocessor

    pp = DataPreprocessor()
    df = pd.read_csv("data/student_data.csv")

    # Validate
    valid, msg = pp.validate_dataset(df)
    assert valid, f"Dataset invalid: {msg}"

    # Inject missing value and clean
    df.loc[0, "study_hours"] = np.nan
    df_clean = pp.handle_missing_values(df)
    assert df_clean.isnull().sum().sum() == 0, "Still has missing values"

    # Full preprocessing
    df2 = pd.read_csv("data/student_data.csv")
    X, y, feats = pp.preprocess(df2, fit=True)
    assert X.shape[0] == 150
    assert X.shape[1] > 0
    assert pp.is_fitted

    # Single input preparation
    xi = pp.prepare_single_input({
        "study_hours": 5.0,
        "attendance": 80.0,
        "previous_marks": 65.0,
        "participation": "High",
    })
    assert xi.shape == (1, len(pp.feature_columns)), f"Shape mismatch: {xi.shape}"
    return f"features={feats}, shape={X.shape}"

run_test("4_preprocessing", t_preprocess)


# ─── TEST 5: Model Training ─────────────────────────────────
def t_training():
    from src.train import ModelTrainer

    trainer = ModelTrainer(model_dir="models")
    res = trainer.full_training_pipeline("data/student_data.csv")

    assert "results" in res
    assert "best_model" in res
    best = res["best_model"]
    assert best in ["Linear Regression", "Decision Tree", "Random Forest"]

    for name, m in res["results"].items():
        assert "mae" in m
        assert "rmse" in m
        assert "r2_score" in m
        assert m["r2_score"] > 0, f"{name} R2={m['r2_score']}"

    assert os.path.exists("models/best_model.joblib")
    assert os.path.exists("models/preprocessor.joblib")
    assert os.path.exists("models/model_metadata.json")

    # Print all model R2s
    scores = {n: m["r2_score"] for n, m in res["results"].items()}
    return f"best={best}, R2s={scores}"

run_test("5_model_training", t_training)


# ─── TEST 6: Prediction (basic) ─────────────────────────────
def t_predict_basic():
    from src.predict import StudentPredictor

    p = StudentPredictor(model_dir="models")
    ok = p.load_model()
    assert ok, "load_model() returned False"
    assert p.is_loaded

    val = p.predict({
        "study_hours": 6.0,
        "attendance": 85.0,
        "previous_marks": 72.0,
        "participation": "High",
    })
    assert isinstance(val, float), f"Expected float, got {type(val)}"
    assert 0 <= val <= 100, f"Out of range: {val}"
    return f"predicted={val}"

run_test("6_predict_basic", t_predict_basic)


# ─── TEST 7: Prediction (edge cases) ────────────────────────
def t_predict_edge():
    from src.predict import StudentPredictor

    p = StudentPredictor(model_dir="models")
    p.load_model()

    low = p.predict({"study_hours": 0.0, "attendance": 30.0,
                     "previous_marks": 20.0, "participation": "Low"})
    high = p.predict({"study_hours": 12.0, "attendance": 100.0,
                      "previous_marks": 100.0, "participation": "High"})

    assert 0 <= low <= 100,  f"Low out of range: {low}"
    assert 0 <= high <= 100, f"High out of range: {high}"
    assert high > low, f"high({high}) not > low({low})"
    return f"low={low}, high={high}"

run_test("7_predict_edge_cases", t_predict_edge)


# ─── TEST 8: Model Info ─────────────────────────────────────
def t_model_info():
    from src.predict import StudentPredictor

    p = StudentPredictor(model_dir="models")
    p.load_model()
    info = p.get_model_info()
    assert "best_model" in info
    assert "metrics" in info
    r2 = p.get_best_r2()
    assert r2 > 0, f"R2 too low: {r2}"
    return f"best={info['best_model']}, R2={r2}"

run_test("8_model_info", t_model_info)


# ─── TEST 9: Prediction History ─────────────────────────────
def t_history():
    from src.utils import save_prediction_history, load_prediction_history

    hf = "data/test_hist.json"
    if os.path.exists(hf):
        os.remove(hf)

    save_prediction_history({"predicted_marks": 77.5, "study_hours": 5}, history_file=hf)
    save_prediction_history({"predicted_marks": 82.0, "study_hours": 7}, history_file=hf)
    hist = load_prediction_history(hf)
    assert len(hist) == 2
    assert hist[0]["predicted_marks"] == 77.5
    assert "timestamp" in hist[0]
    os.remove(hf)
    return "2 records saved and loaded correctly"

run_test("9_prediction_history", t_history)


# ─── TEST 10: Visualization (headless) ───────────────────────
def t_viz():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np

    df = pd.read_csv("data/student_data.csv")
    num = df.select_dtypes(include=[np.number])

    fig1, ax1 = plt.subplots()
    sns.heatmap(num.corr(), ax=ax1)
    plt.close(fig1)

    fig2, ax2 = plt.subplots()
    sns.histplot(df["marks"], kde=True, ax=ax2)
    plt.close(fig2)

    fig3, ax3 = plt.subplots()
    ax3.barh(["a", "b", "c"], [0.3, 0.5, 0.7])
    plt.close(fig3)
    return "heatmap, histogram, barh all created"

run_test("10_visualizations", t_viz)


# ─── TEST 11: app.py syntax ──────────────────────────────────
def t_app_syntax():
    import ast
    with open("app.py", "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    assert tree is not None
    return f"{len(src)} bytes parsed OK"

run_test("11_app_syntax", t_app_syntax)


# ─────────────────────────────────────────────────────────────
# Write results to JSON
# ─────────────────────────────────────────────────────────────
with open("test_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

# Print summary
passed  = [k for k, v in results.items() if v.startswith("PASS") and not k.endswith("_tb")]
failed  = [k for k, v in results.items() if v.startswith("FAIL") and not k.endswith("_tb")]
total   = len(passed) + len(failed)

print(f"\nResults written to test_results.json")
print(f"Passed: {len(passed)}/{total}")
print(f"Failed: {len(failed)}/{total}")
if failed:
    print("\nFailed tests:")
    for k in failed:
        print(f"  {k}: {results[k][:200]}")
    sys.exit(1)
else:
    print("ALL TESTS PASSED")
