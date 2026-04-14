# Model Data Code Documentation

## Overview

This document contains all the code and documentation for the Student Performance Predictor machine learning models. The system uses three regression models to predict student GPA based on 12 input features.

---

---

## Data Insights & Exploratory Analysis

### GPA Performance Statistics
- **Median GPA**: 1.89 (0-4.0 Scale)
- **Standard Deviation**: 0.92
- **Range**: 0.0 to 4.0
- **Average Weekly Study Time**: 9.8 hours
- **Average Absences**: 14.5 days per period

### Student Lifestyle Participation
- **Tutoring Support**: 29.9% of students receive additional tutoring.
- **Extracurricular Activities**: 38.1% of students participating.
- **Sports Involvement**: 30.2% of the student body.
- **Music Interest**: 19.5% of students.
- **Volunteering**: 15.7% engage in community service.

---

## Student Grade Distribution

Based on the dataset of 2,411 students, the following grade distribution is observed:

| Grade | GPA Range | Student Count | Percentage |
|-------|-----------|---------------|------------|
| **Grade A** | 3.5 - 4.0 | 107 | 4.4% |
| **Grade B** | 3.0 - 3.5 | 271 | 11.2% |
| **Grade C** | 2.5 - 3.0 | 396 | 16.4% |
| **Grade D** | 2.0 - 2.5 | 526 | 21.8% |
| **Grade F** | < 2.0 | 1,111 | 46.1% |

---

## Demographic Overview

### Diversity & Background
- **Gender Balance**: 51.5% Male (1,241) and 48.5% Female (1,170).
- **Parental Education**: 
    - Most common: "Some College" (38.7%)
    - Average Support Rating: 2.1 / 4.0


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

The system utilizes standard regression algorithms to identify linear patterns in student data. 

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

The model evaluates non-linear relationships using hierarchical decision rules (maximum depth of 10).

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

An ensemble of 100 decision trees is used to provide robust predictions and minimize overfitting.

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

- Student records are loaded securely from the CSV dataset.


2. **Remove Non-Features**
   - Drop `StudentID` (not a predictive feature)
   - Drop `GradeClass` (derived from GPA)

3. **Handle Missing Values**
   - Numerical columns: Fill with median
   - Categorical columns: Fill with mode

- Features are normalized using standard scaling to ensure uniform model evaluation.


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

The retraining process involves loading 2,410 records, performing automatic preprocessing, and evaluating model accuracy across multiple algorithms. The best performing model (typically Linear Regression) is then automatically saved for production use.


---

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

- Run the training module to update prediction weights.


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
