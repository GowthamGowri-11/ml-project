"""
Data Manager - Handle dynamic dataset updates
Automatically saves predictions to the dataset and tracks growth
"""

import os
import pandas as pd
from datetime import datetime
import json


class DataManager:
    """Manages dataset updates and tracks data growth"""
    
    def __init__(self, dataset_path="dataset/Student_performance_data _.csv"):
        self.dataset_path = dataset_path
        self.stats_path = "data/dataset_stats.json"
        
    def load_dataset(self):
        """Load the current dataset"""
        if os.path.exists(self.dataset_path):
            return pd.read_csv(self.dataset_path)
        return None
    
    def get_dataset_stats(self):
        """Get current dataset statistics"""
        df = self.load_dataset()
        if df is None:
            return {"total_records": 0, "last_updated": None}
        
        stats = {
            "total_records": len(df),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "features": list(df.columns),
            "gpa_range": [float(df["GPA"].min()), float(df["GPA"].max())],
            "avg_gpa": float(df["GPA"].mean())
        }
        
        # Save stats
        os.makedirs(os.path.dirname(self.stats_path), exist_ok=True)
        with open(self.stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
        
        return stats
    
    def add_prediction_to_dataset(self, student_data, predicted_gpa, actual_gpa=None):
        """
        Add a new prediction to the dataset
        
        Args:
            student_data (dict): Student features (Age, Gender, etc.)
            predicted_gpa (float): Predicted GPA (0-10 scale)
            actual_gpa (float, optional): Actual GPA if known
        
        Returns:
            dict: Updated statistics
        """
        df = self.load_dataset()
        
        if df is None:
            print("❌ Dataset not found!")
            return None
        
        # Get the next StudentID
        max_id = df["StudentID"].max() if "StudentID" in df.columns else 0
        new_id = max_id + 1
        
        # Convert predicted GPA from 0-10 scale to 0-4 scale
        gpa_4_scale = predicted_gpa / 2.5
        
        # Use actual GPA if provided, otherwise use predicted
        final_gpa = actual_gpa / 2.5 if actual_gpa is not None else gpa_4_scale
        
        # Determine grade class
        if final_gpa >= 3.5:
            grade_class = 0  # A
        elif final_gpa >= 3.0:
            grade_class = 1  # B
        elif final_gpa >= 2.5:
            grade_class = 2  # C
        elif final_gpa >= 2.0:
            grade_class = 3  # D
        else:
            grade_class = 4  # F
        
        # Create new record
        new_record = {
            "StudentID": new_id,
            "Age": student_data.get("Age", 17),
            "Gender": student_data.get("Gender", 0),
            "Ethnicity": student_data.get("Ethnicity", 0),
            "ParentalEducation": student_data.get("ParentalEducation", 2),
            "StudyTimeWeekly": student_data.get("StudyTimeWeekly", 10.0),
            "Absences": student_data.get("Absences", 5),
            "Tutoring": student_data.get("Tutoring", 0),
            "ParentalSupport": student_data.get("ParentalSupport", 2),
            "Extracurricular": student_data.get("Extracurricular", 0),
            "Sports": student_data.get("Sports", 0),
            "Music": student_data.get("Music", 0),
            "Volunteering": student_data.get("Volunteering", 0),
            "GPA": round(final_gpa, 4),
            "GradeClass": grade_class
        }
        
        # Append to dataframe
        new_df = pd.DataFrame([new_record])
        df = pd.concat([df, new_df], ignore_index=True)
        
        # Save updated dataset
        df.to_csv(self.dataset_path, index=False)
        
        # Update stats
        stats = self.get_dataset_stats()
        
        print(f"✅ Added new record! Dataset now has {stats['total_records']} students")
        
        return stats
    
    def get_growth_info(self):
        """Get information about dataset growth"""
        if os.path.exists(self.stats_path):
            with open(self.stats_path, 'r') as f:
                stats = json.load(f)
            return stats
        return None
    
    def check_retrain_needed(self, threshold=100):
        """
        Check if model retraining is needed based on new data
        
        Args:
            threshold (int): Number of new records before retraining
        
        Returns:
            bool: True if retraining is recommended
        """
        # This would compare current size with size at last training
        # For now, return False (manual retraining)
        return False


# Convenience functions
def add_prediction(student_data, predicted_gpa, actual_gpa=None):
    """Add a prediction to the dataset"""
    manager = DataManager()
    return manager.add_prediction_to_dataset(student_data, predicted_gpa, actual_gpa)


def get_dataset_info():
    """Get current dataset information"""
    manager = DataManager()
    return manager.get_dataset_stats()


def get_record_count():
    """Get total number of records"""
    manager = DataManager()
    stats = manager.get_dataset_stats()
    return stats["total_records"] if stats else 0
