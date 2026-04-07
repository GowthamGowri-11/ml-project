# 🎓 Student Performance Predictor

A machine learning web application that predicts student academic performance (marks) based on various input factors like study hours, attendance, and previous performance.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange?logo=scikit-learn)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

### 3. Use the App

1. **Generate Sample Data** or upload your own CSV
2. Click **Train Models** in the sidebar
3. Enter student details and click **Predict Marks**

---

## 📁 Project Structure

```
student-performance-predictor/
│
├── data/                    # Dataset storage
│   └── student_data.csv     # Generated/uploaded dataset
│   └── prediction_history.json
│
├── models/                  # Saved trained models
│   ├── best_model.joblib
│   ├── preprocessor.joblib
│   └── model_metadata.json
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py     # Data cleaning & encoding
│   ├── train.py             # Model training & evaluation
│   ├── predict.py           # Prediction logic
│   └── utils.py             # Helper functions
│
├── app.py                   # Main Streamlit UI
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 🤖 Machine Learning Pipeline

### Models Used
- **Linear Regression** — Simple baseline model
- **Decision Tree Regressor** — Captures non-linear patterns
- **Random Forest Regressor** — Ensemble for robust predictions

### Evaluation Metrics
- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **R² Score** (Coefficient of Determination)

The system **automatically selects the best model** based on R² score.

---

## 📊 Features

- ✅ Real-time student mark prediction
- ✅ Multiple model comparison
- ✅ Data visualization (heatmaps, distributions)
- ✅ Feature importance analysis
- ✅ Prediction history tracking
- ✅ CSV upload support
- ✅ Sample data generation
- ✅ Dark / Light mode toggle
- ✅ Download prediction results

---

## 📝 Dataset Format

Your CSV should include these columns:

| Column | Type | Description |
|--------|------|-------------|
| `study_hours` | float | Daily study hours (0-12) |
| `attendance` | float | Attendance percentage (0-100) |
| `previous_marks` | float | Previous exam marks (0-100) |
| `participation` | string | Low / Medium / High (optional) |
| `marks` | float | Target — actual marks (0-100) |

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** — Web UI
- **Scikit-learn** — ML Models
- **Pandas / NumPy** — Data Processing
- **Matplotlib / Seaborn** — Visualizations
- **Joblib** — Model Serialization

---

## 📄 License

This project is for educational purposes.
