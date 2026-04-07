"""
utils.py - Helper functions for the Student Performance Predictor.

Contains utility functions used across the project for
classification, formatting, and common operations.
"""

import os
import json
import pandas as pd
from datetime import datetime


def classify_performance(marks):
    """
    Classify student performance based on predicted marks.

    Args:
        marks (float): Predicted marks (0-100).

    Returns:
        tuple: (category_label, emoji, color)
    """
    if marks >= 85:
        return "Excellent 🌟", "🌟", "#00c853"
    elif marks >= 70:
        return "High ✅", "✅", "#2979ff"
    elif marks >= 50:
        return "Medium ⚠️", "⚠️", "#ff9100"
    elif marks >= 35:
        return "Low 📉", "📉", "#ff5252"
    else:
        return "Very Low ❌", "❌", "#d50000"


def get_confidence_level(r2_score, prediction, min_val=0, max_val=100):
    """
    Calculate a confidence indicator for the prediction.

    Uses the model's R² score and whether the prediction falls
    within a reasonable range.

    Args:
        r2_score (float): The R² score of the model.
        prediction (float): The predicted value.
        min_val (float): Minimum expected value.
        max_val (float): Maximum expected value.

    Returns:
        tuple: (confidence_percentage, confidence_label, color)
    """
    # Base confidence from R² score (0-100%)
    base_confidence = max(0, r2_score) * 100

    # Penalize if prediction is out of expected range
    if prediction < min_val or prediction > max_val:
        base_confidence *= 0.7

    # Classify confidence level
    if base_confidence >= 80:
        return base_confidence, "High Confidence", "#00c853"
    elif base_confidence >= 60:
        return base_confidence, "Moderate Confidence", "#ff9100"
    else:
        return base_confidence, "Low Confidence", "#ff5252"


def format_metric(value, decimals=2):
    """Format a metric value to specified decimal places."""
    return round(float(value), decimals)


def validate_input(study_hours, attendance, previous_marks):
    """
    Validate user input values.

    Args:
        study_hours (float): Hours of study per day.
        attendance (float): Attendance percentage.
        previous_marks (float): Previous exam marks.

    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []

    if study_hours < 0 or study_hours > 24:
        errors.append("Study hours must be between 0 and 24.")

    if attendance < 0 or attendance > 100:
        errors.append("Attendance must be between 0% and 100%.")

    if previous_marks < 0 or previous_marks > 100:
        errors.append("Previous marks must be between 0 and 100.")

    if errors:
        return False, " | ".join(errors)
    return True, ""


def save_prediction_history(prediction_data, history_file="data/prediction_history.json"):
    """
    Save a prediction to the history file.

    Args:
        prediction_data (dict): Dictionary with prediction details.
        history_file (str): Path to the history JSON file.
    """
    # Add timestamp
    prediction_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Load existing history
    history = load_prediction_history(history_file)
    history.append(prediction_data)

    # Save updated history
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)


def load_prediction_history(history_file="data/prediction_history.json"):
    """
    Load prediction history from file.

    Args:
        history_file (str): Path to the history JSON file.

    Returns:
        list: List of prediction dictionaries.
    """
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def generate_sample_dataset(n_samples=200, save_path="data/student_data.csv"):
    """
    Generate a realistic synthetic dataset for testing.

    This creates a dataset where marks are influenced by
    study_hours, attendance, and previous_marks with some noise.

    Args:
        n_samples (int): Number of samples to generate.
        save_path (str): Path to save the CSV file.

    Returns:
        pd.DataFrame: The generated dataset.
    """
    import numpy as np

    np.random.seed(42)

    # Generate features
    study_hours = np.random.uniform(0, 12, n_samples)
    attendance = np.random.uniform(30, 100, n_samples)
    previous_marks = np.random.uniform(20, 100, n_samples)

    # Participation levels (categorical)
    participation_levels = np.random.choice(
        ["Low", "Medium", "High"], n_samples, p=[0.25, 0.45, 0.30]
    )

    # Encode participation for marks calculation
    participation_encoded = np.where(
        participation_levels == "High", 1.5,
        np.where(participation_levels == "Medium", 1.0, 0.5)
    )

    # Generate marks with a realistic formula + noise
    marks = (
        study_hours * 3.5 +           # Study hours contribution
        attendance * 0.3 +              # Attendance contribution
        previous_marks * 0.35 +         # Previous marks contribution
        participation_encoded * 5 +     # Participation bonus
        np.random.normal(0, 5, n_samples)  # Random noise
    )

    # Clip marks to 0-100 range
    marks = np.clip(marks, 0, 100)

    # Create DataFrame
    df = pd.DataFrame({
        "study_hours": np.round(study_hours, 1),
        "attendance": np.round(attendance, 1),
        "previous_marks": np.round(previous_marks, 1),
        "participation": participation_levels,
        "marks": np.round(marks, 1)
    })

    # Save to CSV
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"[OK] Sample dataset saved to {save_path} ({n_samples} records)")

    return df
