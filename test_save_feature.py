"""
Test script to verify the save to dataset feature works correctly
"""

import pandas as pd
from src.data_manager import DataManager

# Initialize data manager
dm = DataManager()

# Get current count
print("=" * 60)
print("TESTING SAVE TO DATASET FEATURE")
print("=" * 60)

# Load current dataset
df = pd.read_csv("dataset/Student_performance_data _.csv")
initial_count = len(df)
print(f"\n📊 Initial dataset count: {initial_count}")

# Create test student data
test_student = {
    "Age": 17,
    "Gender": 1,
    "Ethnicity": 0,
    "ParentalEducation": 3,
    "StudyTimeWeekly": 12.0,
    "Absences": 3,
    "Tutoring": 1,
    "ParentalSupport": 4,
    "Extracurricular": 1,
    "Sports": 1,
    "Music": 0,
    "Volunteering": 1
}

predicted_gpa = 8.5  # On 0-10 scale

print(f"\n🧑‍🎓 Test student data:")
for key, value in test_student.items():
    print(f"   {key}: {value}")
print(f"   Predicted GPA: {predicted_gpa}")

# Save to dataset
print(f"\n💾 Saving to dataset...")
stats = dm.add_prediction_to_dataset(test_student, predicted_gpa)

if stats:
    print(f"\n✅ SUCCESS!")
    print(f"   Total records: {stats['total_records']}")
    print(f"   Last updated: {stats['last_updated']}")
    print(f"   Records added: {stats['total_records'] - initial_count}")
    
    # Verify by reading the file again
    df_new = pd.read_csv("dataset/Student_performance_data _.csv")
    final_count = len(df_new)
    
    print(f"\n🔍 Verification:")
    print(f"   Initial count: {initial_count}")
    print(f"   Final count: {final_count}")
    print(f"   Difference: +{final_count - initial_count}")
    
    # Show the last record
    print(f"\n📋 Last record in dataset:")
    last_record = df_new.iloc[-1]
    print(f"   StudentID: {last_record['StudentID']}")
    print(f"   Age: {last_record['Age']}")
    print(f"   StudyTimeWeekly: {last_record['StudyTimeWeekly']}")
    print(f"   GPA: {last_record['GPA']} (0-4 scale)")
    print(f"   GradeClass: {last_record['GradeClass']}")
    
    if final_count == initial_count + 1:
        print(f"\n🎉 TEST PASSED! Record successfully added to dataset.")
    else:
        print(f"\n❌ TEST FAILED! Expected {initial_count + 1} records, got {final_count}")
else:
    print(f"\n❌ FAILED! No stats returned")

print("\n" + "=" * 60)
