"""
app.py - Main Streamlit Application for Student Performance Predictor.

A modern, professional dashboard for predicting student academic
performance using machine learning models.

Features:
- Real-time prediction via interactive UI
- Data visualization (heatmaps, charts)
- Model evaluation & comparison
- Prediction history tracking
- Dataset upload support
- Dark/Light mode toggle
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.preprocessing import DataPreprocessor
from src.train import ModelTrainer
from src.predict import StudentPredictor
from src.utils import (
    classify_performance,
    get_confidence_level,
    format_metric,
    validate_input,
    save_prediction_history,
    load_prediction_history,
    generate_sample_dataset,
)

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="🎓 Student Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS STYLING
# ============================================================
def inject_custom_css(dark_mode=False):
    """Inject custom CSS for a premium UI look."""

    if dark_mode:
        bg_primary = "#0e1117"
        bg_secondary = "#1a1d24"
        bg_card = "#1e2129"
        text_primary = "#fafafa"
        text_secondary = "#b0b8c8"
        accent = "#6c63ff"
        accent_light = "#8b83ff"
        border_color = "#2d3139"
        gradient_start = "#6c63ff"
        gradient_end = "#3b82f6"
    else:
        bg_primary = "#f8f9fc"
        bg_secondary = "#ffffff"
        bg_card = "#ffffff"
        text_primary = "#1a1a2e"
        text_secondary = "#64748b"
        accent = "#6c63ff"
        accent_light = "#8b83ff"
        border_color = "#e2e8f0"
        gradient_start = "#6c63ff"
        gradient_end = "#3b82f6"

    st.markdown(f"""
    <style>
        /* ---- Global Styles ---- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        .stApp {{
            font-family: 'Inter', sans-serif;
        }}

        /* ---- Header Banner ---- */
        .header-banner {{
            background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%);
            padding: 2rem 2.5rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            color: white;
            position: relative;
            overflow: hidden;
        }}
        .header-banner::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 300px;
            height: 300px;
            background: rgba(255,255,255,0.08);
            border-radius: 50%;
        }}
        .header-banner::after {{
            content: '';
            position: absolute;
            bottom: -30%;
            left: 10%;
            width: 200px;
            height: 200px;
            background: rgba(255,255,255,0.05);
            border-radius: 50%;
        }}
        .header-banner h1 {{
            font-size: 2rem;
            font-weight: 800;
            margin: 0 0 0.3rem 0;
            letter-spacing: -0.5px;
            position: relative;
            z-index: 1;
        }}
        .header-banner p {{
            font-size: 1rem;
            opacity: 0.9;
            margin: 0;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }}

        /* ---- Metric Cards ---- */
        .metric-card {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 14px;
            padding: 1.3rem 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        .metric-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(108, 99, 255, 0.15);
        }}
        .metric-card .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            color: {accent};
            line-height: 1.2;
        }}
        .metric-card .metric-label {{
            font-size: 0.85rem;
            color: {text_secondary};
            font-weight: 500;
            margin-top: 0.3rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        /* ---- Prediction Result Card ---- */
        .prediction-card {{
            background: linear-gradient(135deg, {gradient_start}15 0%, {gradient_end}15 100%);
            border: 2px solid {accent};
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            margin: 1rem 0;
        }}
        .prediction-card .pred-value {{
            font-size: 3.5rem;
            font-weight: 800;
            color: {accent};
            line-height: 1;
        }}
        .prediction-card .pred-label {{
            font-size: 1rem;
            color: {text_secondary};
            margin-top: 0.5rem;
            font-weight: 500;
        }}

        /* ---- Section Title ---- */
        .section-title {{
            font-size: 1.3rem;
            font-weight: 700;
            color: {text_primary};
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid {accent};
            display: inline-block;
        }}

        /* ---- Info Badge ---- */
        .badge {{
            display: inline-block;
            padding: 0.35rem 0.9rem;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
            letter-spacing: 0.3px;
        }}
        .badge-success {{
            background: #00c85320;
            color: #00c853;
            border: 1px solid #00c85340;
        }}
        .badge-warning {{
            background: #ff910020;
            color: #ff9100;
            border: 1px solid #ff910040;
        }}
        .badge-danger {{
            background: #ff525220;
            color: #ff5252;
            border: 1px solid #ff525240;
        }}
        .badge-info {{
            background: #2979ff20;
            color: #2979ff;
            border: 1px solid #2979ff40;
        }}

        /* ---- Sidebar Styling ---- */
        section[data-testid="stSidebar"] {{
            background: {bg_secondary};
            border-right: 1px solid {border_color};
        }}

        /* ---- Hide default Streamlit elements ---- */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* ---- Smooth transitions ---- */
        * {{
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        /* ---- Rounded plots ---- */
        .stPlotlyChart, .element-container img {{
            border-radius: 12px;
            overflow: hidden;
        }}
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS FOR UI
# ============================================================

def render_header():
    """Render the main header banner."""
    st.markdown("""
    <div class="header-banner">
        <h1>🎓 Student Performance Predictor</h1>
        <p>AI-powered academic performance prediction using Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label, value, col):
    """Render a styled metric card."""
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)


def render_prediction_result(predicted_marks, category, confidence_pct, confidence_label, conf_color):
    """Render the prediction result card."""
    # Determine badge class
    if "High" in category or "Excellent" in category:
        badge_class = "badge-success"
    elif "Medium" in category:
        badge_class = "badge-warning"
    else:
        badge_class = "badge-danger"

    # Confidence badge
    if confidence_pct >= 80:
        conf_badge = "badge-success"
    elif confidence_pct >= 60:
        conf_badge = "badge-warning"
    else:
        conf_badge = "badge-danger"

    st.markdown(f"""
    <div class="prediction-card">
        <div class="pred-label">PREDICTED MARKS</div>
        <div class="pred-value">{predicted_marks:.1f}</div>
        <div style="margin-top: 1rem;">
            <span class="badge {badge_class}">{category}</span>
            &nbsp;&nbsp;
            <span class="badge {conf_badge}">{confidence_label}: {confidence_pct:.0f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# VISUALIZATION FUNCTIONS
# ============================================================

def plot_correlation_heatmap(df):
    """Plot a correlation heatmap for numerical features."""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Select only numerical columns
    numeric_df = df.select_dtypes(include=[np.number])

    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="RdYlBu_r",
        center=0,
        fmt=".2f",
        linewidths=0.5,
        square=True,
        ax=ax,
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    return fig


def plot_feature_importance(importance_dict):
    """Plot feature importance as a horizontal bar chart."""
    if importance_dict is None:
        return None

    features = list(importance_dict.keys())
    importances = list(importance_dict.values())

    # Sort by importance
    sorted_idx = np.argsort(importances)
    features = [features[i] for i in sorted_idx]
    importances = [importances[i] for i in sorted_idx]

    fig, ax = plt.subplots(figsize=(8, 5))

    colors = plt.cm.RdYlBu_r(np.linspace(0.3, 0.9, len(features)))
    bars = ax.barh(features, importances, color=colors, edgecolor="white", linewidth=0.5, height=0.6)

    ax.set_xlabel("Importance", fontsize=11, fontweight="500")
    ax.set_title("Feature Importance", fontsize=14, fontweight="bold", pad=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Add value labels
    for bar, val in zip(bars, importances):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
                f"{val:.3f}", va="center", fontsize=10, fontweight="500")

    plt.tight_layout()
    return fig


def plot_model_comparison(results):
    """Plot a model comparison chart."""
    model_names = list(results.keys())
    mae_values = [results[m]["mae"] for m in model_names]
    rmse_values = [results[m]["rmse"] for m in model_names]
    r2_values = [results[m]["r2_score"] for m in model_names]

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    # Color palette
    colors = ["#6c63ff", "#3b82f6", "#06b6d4"]

    # MAE Chart
    bars1 = axes[0].bar(model_names, mae_values, color=colors, edgecolor="white", linewidth=1)
    axes[0].set_title("MAE (Lower is Better)", fontsize=12, fontweight="bold", pad=10)
    axes[0].set_ylabel("MAE")
    for bar, val in zip(bars1, mae_values):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                     f"{val:.2f}", ha="center", fontsize=9, fontweight="600")

    # RMSE Chart
    bars2 = axes[1].bar(model_names, rmse_values, color=colors, edgecolor="white", linewidth=1)
    axes[1].set_title("RMSE (Lower is Better)", fontsize=12, fontweight="bold", pad=10)
    axes[1].set_ylabel("RMSE")
    for bar, val in zip(bars2, rmse_values):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                     f"{val:.2f}", ha="center", fontsize=9, fontweight="600")

    # R² Chart
    bars3 = axes[2].bar(model_names, r2_values, color=colors, edgecolor="white", linewidth=1)
    axes[2].set_title("R² Score (Higher is Better)", fontsize=12, fontweight="bold", pad=10)
    axes[2].set_ylabel("R² Score")
    for bar, val in zip(bars3, r2_values):
        axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                     f"{val:.4f}", ha="center", fontsize=9, fontweight="600")

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha="right", fontsize=9)

    plt.tight_layout()
    return fig


def plot_actual_vs_predicted(y_test, y_pred):
    """Plot actual vs predicted marks scatter chart."""
    fig, ax = plt.subplots(figsize=(7, 6))

    ax.scatter(y_test, y_pred, alpha=0.6, color="#6c63ff", edgecolors="white",
               linewidth=0.5, s=60, label="Predictions")

    # Perfect prediction line
    min_val = min(min(y_test), min(y_pred))
    max_val = max(max(y_test), max(y_pred))
    ax.plot([min_val, max_val], [min_val, max_val], "--", color="#ff5252",
            linewidth=2, alpha=0.8, label="Perfect Prediction")

    ax.set_xlabel("Actual Marks", fontsize=12, fontweight="500")
    ax.set_ylabel("Predicted Marks", fontsize=12, fontweight="500")
    ax.set_title("Actual vs Predicted Marks", fontsize=14, fontweight="bold", pad=15)
    ax.legend(frameon=True, fancybox=True, shadow=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    return fig


def plot_input_vs_prediction(input_data, prediction):
    """Plot a radar/comparison chart of inputs vs prediction."""
    categories = list(input_data.keys())
    values = list(input_data.values())

    # Normalize all values to 0-100 scale for comparison
    normalized = []
    for key, val in input_data.items():
        if key == "study_hours":
            normalized.append((val / 12) * 100)  # Max 12 hours
        elif key == "attendance":
            normalized.append(val)
        elif key == "previous_marks":
            normalized.append(val)
        elif key == "participation":
            mapping = {"Low": 25, "Medium": 50, "High": 75}
            normalized.append(mapping.get(val, 50))
        else:
            normalized.append(val)

    # Add prediction
    categories.append("Predicted Marks")
    normalized.append(prediction)

    fig, ax = plt.subplots(figsize=(8, 5))
    colors_list = ["#6c63ff", "#3b82f6", "#06b6d4", "#8b5cf6", "#f59e0b"]
    bars = ax.bar(categories, normalized, color=colors_list[:len(categories)],
                  edgecolor="white", linewidth=1, width=0.6)

    ax.set_ylabel("Value (Normalized to 0-100)", fontsize=11)
    ax.set_title("Input Features vs Prediction", fontsize=14, fontweight="bold", pad=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, 110)

    for bar, val in zip(bars, normalized):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f"{val:.1f}", ha="center", fontsize=10, fontweight="600")

    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    return fig


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def init_session_state():
    """Initialize Streamlit session state variables."""
    defaults = {
        "model_trained": False,
        "trainer": None,
        "predictor": None,
        "training_results": None,
        "dataset": None,
        "dark_mode": True,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    """Main application entry point."""
    init_session_state()

    # Apply custom CSS
    inject_custom_css(dark_mode=st.session_state.dark_mode)

    # ---- SIDEBAR ----
    with st.sidebar:
        st.markdown("## ⚙️ Controls")
        st.markdown("---")

        # Dark/Light mode toggle
        dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()

        st.markdown("---")
        st.markdown("### 📂 Dataset")

        # Dataset source selection
        data_source = st.radio(
            "Choose data source:",
            ["📁 Upload CSV", "🧪 Generate Sample Data", "📂 Use Existing File"],
            index=1,
        )

        dataset_loaded = False

        if data_source == "📁 Upload CSV":
            uploaded_file = st.file_uploader(
                "Upload your CSV file",
                type=["csv"],
                help="CSV must contain: study_hours, attendance, previous_marks, marks",
            )
            if uploaded_file is not None:
                try:
                    st.session_state.dataset = pd.read_csv(uploaded_file)
                    dataset_loaded = True
                    st.success(f"✅ Loaded {len(st.session_state.dataset)} records")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

        elif data_source == "🧪 Generate Sample Data":
            n_samples = st.slider("Number of samples", 50, 500, 200, 50)
            if st.button("🔄 Generate Dataset", use_container_width=True):
                with st.spinner("Generating sample data..."):
                    st.session_state.dataset = generate_sample_dataset(
                        n_samples=n_samples,
                        save_path="data/student_data.csv"
                    )
                    dataset_loaded = True
                    st.success(f"✅ Generated {n_samples} records")

            # Auto-load if dataset already exists
            if st.session_state.dataset is not None:
                dataset_loaded = True

        elif data_source == "📂 Use Existing File":
            file_path = st.text_input(
                "CSV file path",
                value="data/student_data.csv",
            )
            if st.button("📂 Load File", use_container_width=True):
                if os.path.exists(file_path):
                    try:
                        st.session_state.dataset = pd.read_csv(file_path)
                        dataset_loaded = True
                        st.success(f"✅ Loaded {len(st.session_state.dataset)} records")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.error("❌ File not found. Generate sample data first.")

            if st.session_state.dataset is not None:
                dataset_loaded = True

        st.markdown("---")

        # Train model button
        st.markdown("### 🏋️ Model Training")
        if st.button("🚀 Train Models", use_container_width=True, type="primary"):
            if st.session_state.dataset is not None:
                with st.spinner("Training models... This may take a moment."):
                    try:
                        trainer = ModelTrainer(model_dir="models")

                        # Save dataset temporarily
                        os.makedirs("data", exist_ok=True)
                        st.session_state.dataset.to_csv("data/student_data.csv", index=False)

                        # Run training pipeline
                        results = trainer.full_training_pipeline("data/student_data.csv")

                        # Update session state
                        st.session_state.trainer = trainer
                        st.session_state.training_results = results
                        st.session_state.model_trained = True

                        # Initialize predictor
                        predictor = StudentPredictor(model_dir="models")
                        predictor.load_model()
                        st.session_state.predictor = predictor

                        st.success("✅ Models trained successfully!")
                    except Exception as e:
                        st.error(f"❌ Training failed: {str(e)}")
            else:
                st.warning("⚠️ Load a dataset first!")

        # Auto-load existing model
        if not st.session_state.model_trained and os.path.exists("models/best_model.joblib"):
            try:
                predictor = StudentPredictor(model_dir="models")
                if predictor.load_model():
                    st.session_state.predictor = predictor
                    st.session_state.model_trained = True

                    # Load metadata for display
                    if os.path.exists("models/model_metadata.json"):
                        with open("models/model_metadata.json", "r") as f:
                            metadata = json.load(f)
                            st.session_state.training_results = {
                                "results": {
                                    name: {**metrics, "predictions": []}
                                    for name, metrics in metadata.get("metrics", {}).items()
                                },
                                "best_model": metadata.get("best_model", "Unknown"),
                            }
            except Exception:
                pass

        # Model status indicator
        st.markdown("---")
        if st.session_state.model_trained:
            st.markdown("### 🟢 Model Status: Ready")
            if st.session_state.predictor and st.session_state.predictor.metadata:
                best = st.session_state.predictor.metadata.get("best_model", "N/A")
                st.info(f"🏆 Best Model: **{best}**")
        else:
            st.markdown("### 🔴 Model Status: Not Trained")
            st.info("Train a model to start predicting.")

        st.markdown("---")
        st.markdown(
            "<div style='text-align:center; opacity:0.5; font-size:0.75rem;'>"
            "Built with ❤️ using Streamlit & Scikit-learn"
            "</div>",
            unsafe_allow_html=True,
        )

    # ---- MAIN CONTENT ----
    render_header()

    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔮 Predict",
        "📊 Data Explorer",
        "📈 Model Evaluation",
        "📜 History",
        "ℹ️ About",
    ])

    # ============================================================
    # TAB 1: PREDICTION
    # ============================================================
    with tab1:
        if not st.session_state.model_trained:
            st.warning(
                "⚠️ **No trained model found.** Please load a dataset and "
                "train models using the sidebar controls."
            )
            st.info(
                "💡 **Quick Start:** Select '🧪 Generate Sample Data' in the "
                "sidebar, click 'Generate Dataset', then click 'Train Models'."
            )
        else:
            st.markdown('<div class="section-title">📝 Enter Student Details</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                study_hours = st.slider(
                    "📚 Study Hours (per day)",
                    min_value=0.0,
                    max_value=12.0,
                    value=5.0,
                    step=0.5,
                    help="Average daily study hours",
                )

                attendance = st.slider(
                    "📅 Attendance (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=75.0,
                    step=1.0,
                    help="Class attendance percentage",
                )

            with col2:
                previous_marks = st.number_input(
                    "📝 Previous Marks (0-100)",
                    min_value=0.0,
                    max_value=100.0,
                    value=65.0,
                    step=1.0,
                    help="Marks from previous exam",
                )

                participation = st.selectbox(
                    "🙋 Participation Level",
                    options=["Low", "Medium", "High"],
                    index=1,
                    help="Level of class participation",
                )

            st.markdown("---")

            # Predict button
            if st.button("🔮 Predict Marks", use_container_width=True, type="primary"):
                # Validate input
                is_valid, error_msg = validate_input(study_hours, attendance, previous_marks)

                if not is_valid:
                    st.error(f"❌ {error_msg}")
                else:
                    with st.spinner("Predicting..."):
                        try:
                            # Prepare input
                            input_data = {
                                "study_hours": study_hours,
                                "attendance": attendance,
                                "previous_marks": previous_marks,
                                "participation": participation,
                            }

                            # Make prediction
                            predictor = st.session_state.predictor
                            predicted_marks = predictor.predict(input_data)

                            # Get classification
                            category, emoji, cat_color = classify_performance(predicted_marks)

                            # Get confidence
                            r2 = predictor.get_best_r2()
                            conf_pct, conf_label, conf_color = get_confidence_level(
                                r2, predicted_marks
                            )

                            # Display results
                            render_prediction_result(
                                predicted_marks, category, conf_pct, conf_label, conf_color
                            )

                            # Detail columns
                            c1, c2, c3, c4 = st.columns(4)
                            render_metric_card("📚 Study Hours", f"{study_hours}h", c1)
                            render_metric_card("📅 Attendance", f"{attendance}%", c2)
                            render_metric_card("📝 Previous", f"{previous_marks}", c3)
                            render_metric_card("🙋 Participation", participation, c4)

                            # Input vs Prediction chart
                            st.markdown("---")
                            fig_input = plot_input_vs_prediction(input_data, predicted_marks)
                            st.pyplot(fig_input)
                            plt.close(fig_input)

                            # Save to history
                            save_prediction_history({
                                "study_hours": study_hours,
                                "attendance": attendance,
                                "previous_marks": previous_marks,
                                "participation": participation,
                                "predicted_marks": predicted_marks,
                                "category": category,
                                "confidence": round(conf_pct, 1),
                            })

                        except Exception as e:
                            st.error(f"❌ Prediction error: {str(e)}")

    # ============================================================
    # TAB 2: DATA EXPLORER
    # ============================================================
    with tab2:
        if st.session_state.dataset is not None:
            df = st.session_state.dataset

            st.markdown('<div class="section-title">📊 Dataset Overview</div>', unsafe_allow_html=True)

            # Dataset stats
            c1, c2, c3, c4 = st.columns(4)
            render_metric_card("📋 Records", str(len(df)), c1)
            render_metric_card("📊 Features", str(len(df.columns)), c2)
            render_metric_card("❓ Missing", str(df.isnull().sum().sum()), c3)
            render_metric_card("📈 Avg Marks", f"{df['marks'].mean():.1f}" if 'marks' in df.columns else "N/A", c4)

            st.markdown("---")

            # Data preview
            st.markdown('<div class="section-title">🔍 Data Preview</div>', unsafe_allow_html=True)
            st.dataframe(df.head(20), use_container_width=True)

            # Statistics
            st.markdown('<div class="section-title">📈 Statistical Summary</div>', unsafe_allow_html=True)
            st.dataframe(df.describe().round(2), use_container_width=True)

            # Correlation heatmap
            st.markdown("---")
            st.markdown('<div class="section-title">🔥 Correlation Heatmap</div>', unsafe_allow_html=True)
            fig_heatmap = plot_correlation_heatmap(df)
            st.pyplot(fig_heatmap)
            plt.close(fig_heatmap)

            # Distribution plots
            st.markdown("---")
            st.markdown('<div class="section-title">📊 Feature Distributions</div>', unsafe_allow_html=True)

            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                n_cols = min(len(numeric_cols), 4)
                fig_dist, axes = plt.subplots(1, n_cols, figsize=(4 * n_cols, 4))
                if n_cols == 1:
                    axes = [axes]
                for i, col in enumerate(numeric_cols[:n_cols]):
                    sns.histplot(df[col], kde=True, ax=axes[i], color="#6c63ff", alpha=0.6)
                    axes[i].set_title(col.replace("_", " ").title(), fontsize=11, fontweight="bold")
                    axes[i].spines["top"].set_visible(False)
                    axes[i].spines["right"].set_visible(False)
                plt.tight_layout()
                st.pyplot(fig_dist)
                plt.close(fig_dist)
        else:
            st.info("📂 Load a dataset from the sidebar to explore it here.")

    # ============================================================
    # TAB 3: MODEL EVALUATION
    # ============================================================
    with tab3:
        if st.session_state.training_results is not None:
            results = st.session_state.training_results
            model_results = results.get("results", {})
            best_model_name = results.get("best_model", "Unknown")

            st.markdown('<div class="section-title">🏆 Model Comparison</div>', unsafe_allow_html=True)

            # Best model highlight
            if best_model_name in model_results:
                best_metrics = model_results[best_model_name]
                c1, c2, c3 = st.columns(3)
                render_metric_card(
                    "MAE",
                    format_metric(best_metrics.get("mae", "N/A")),
                    c1,
                )
                render_metric_card(
                    "RMSE",
                    format_metric(best_metrics.get("rmse", "N/A")),
                    c2,
                )
                render_metric_card(
                    "R² Score",
                    format_metric(best_metrics.get("r2_score", "N/A"), 4),
                    c3,
                )

            st.markdown("---")

            # Model comparison table
            st.markdown('<div class="section-title">📋 All Models</div>', unsafe_allow_html=True)

            comparison_data = []
            for name, res in model_results.items():
                is_best = "🏆" if name == best_model_name else ""
                comparison_data.append({
                    "Model": f"{name} {is_best}",
                    "MAE": res.get("mae", "N/A"),
                    "RMSE": res.get("rmse", "N/A"),
                    "R² Score": res.get("r2_score", "N/A"),
                })

            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)

            # Model comparison chart
            st.markdown("---")
            st.markdown('<div class="section-title">📊 Visual Comparison</div>', unsafe_allow_html=True)

            # Filter out entries without proper metrics
            valid_results = {
                k: v for k, v in model_results.items()
                if isinstance(v.get("mae"), (int, float))
            }

            if valid_results:
                fig_comp = plot_model_comparison(valid_results)
                st.pyplot(fig_comp)
                plt.close(fig_comp)

            # Actual vs Predicted plot
            y_test = results.get("y_test")
            y_pred = results.get("y_pred")
            if y_test is not None and y_pred is not None and len(y_test) > 0:
                st.markdown("---")
                st.markdown('<div class="section-title">🎯 Actual vs Predicted</div>', unsafe_allow_html=True)
                fig_avp = plot_actual_vs_predicted(y_test, y_pred)
                st.pyplot(fig_avp)
                plt.close(fig_avp)

            # Feature importance
            if st.session_state.trainer is not None:
                importance = st.session_state.trainer.get_feature_importance()
                if importance:
                    st.markdown("---")
                    st.markdown('<div class="section-title">⭐ Feature Importance</div>', unsafe_allow_html=True)
                    fig_imp = plot_feature_importance(importance)
                    st.pyplot(fig_imp)
                    plt.close(fig_imp)
        else:
            st.info("🏋️ Train models to see evaluation results here.")

    # ============================================================
    # TAB 4: PREDICTION HISTORY
    # ============================================================
    with tab4:
        st.markdown('<div class="section-title">📜 Prediction History</div>', unsafe_allow_html=True)

        history = load_prediction_history()

        if history:
            history_df = pd.DataFrame(history)

            # Summary metrics
            c1, c2, c3 = st.columns(3)
            render_metric_card("Total Predictions", str(len(history)), c1)
            render_metric_card(
                "Avg Predicted Marks",
                f"{history_df['predicted_marks'].mean():.1f}",
                c2,
            )
            render_metric_card(
                "Latest Prediction",
                f"{history_df['predicted_marks'].iloc[-1]:.1f}",
                c3,
            )

            st.markdown("---")

            # Display history table
            st.dataframe(
                history_df.sort_index(ascending=False),
                use_container_width=True,
                hide_index=True,
            )

            # Download button
            csv = history_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Prediction History (CSV)",
                data=csv,
                file_name="prediction_history.csv",
                mime="text/csv",
                use_container_width=True,
            )

            # Clear history
            if st.button("🗑️ Clear History", use_container_width=True):
                if os.path.exists("data/prediction_history.json"):
                    os.remove("data/prediction_history.json")
                    st.success("History cleared!")
                    st.rerun()
        else:
            st.info("📝 No predictions made yet. Start predicting to build history!")

    # ============================================================
    # TAB 5: ABOUT
    # ============================================================
    with tab5:
        st.markdown('<div class="section-title">ℹ️ About This Project</div>', unsafe_allow_html=True)

        st.markdown("""
        ### 🎓 Student Performance Predictor

        This application uses **Machine Learning** to predict student academic
        performance based on various input factors.

        ---

        #### 🔧 How It Works

        1. **Data Input**: Load a dataset or generate sample data
        2. **Model Training**: The system trains 3 ML models and selects the best one
        3. **Prediction**: Enter student details to get predicted marks
        4. **Visualization**: Explore data patterns and model performance

        ---

        #### 🤖 Models Used

        | Model | Description |
        |-------|-------------|
        | **Linear Regression** | Simple, interpretable baseline model |
        | **Decision Tree** | Captures non-linear relationships |
        | **Random Forest** | Ensemble method for robust predictions |

        ---

        #### 📊 Input Features

        | Feature | Type | Range |
        |---------|------|-------|
        | Study Hours | Numerical | 0-12 hrs/day |
        | Attendance | Numerical | 0-100% |
        | Previous Marks | Numerical | 0-100 |
        | Participation | Categorical | Low / Medium / High |

        ---

        #### 🛠️ Tech Stack

        - **Python** - Core language
        - **Streamlit** - UI framework
        - **Scikit-learn** - ML models
        - **Pandas / NumPy** - Data processing
        - **Matplotlib / Seaborn** - Visualizations

        ---

        #### 📝 Dataset Requirements

        Your CSV dataset should contain these columns:
        - `study_hours` - Daily study hours
        - `attendance` - Attendance percentage
        - `previous_marks` - Previous exam marks
        - `participation` - Participation level (optional)
        - `marks` - Target variable (actual marks)

        ---

        <div style="text-align: center; padding: 1rem; opacity: 0.6;">
            Built with ❤️ | Student Performance Predictor v1.0
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# RUN THE APP
# ============================================================
if __name__ == "__main__":
    main()
