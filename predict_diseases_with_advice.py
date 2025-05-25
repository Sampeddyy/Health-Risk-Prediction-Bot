import pandas as pd
import numpy as np
import tensorflow as tf
import pickle

# File paths (updated with your provided addresses)
NUTRIENT_FILE = r'S:\btp\Person Calories Data\Samar shah_2\nutrients_Samar_shah_2.xlsx'
BLOOD_FILE = r'S:\btp\Person Calories Data\Samar shah_2\medical_Samar_shah_2.xlsx'

# Load the trained model and scaler
model = tf.keras.models.load_model('disease_model_tf.keras')
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Define the 37 features the model expects
feature_names = [
    'creatinine', 'gfr_estimated', 'urea', 'urea_nitrogen_blood', 'bun_creatinine_ratio',
    'uric_acid', 'ast', 'alt', 'ggtp', 'alkaline_phosphatase', 'bilirubin_total',
    'bilirubin_direct', 'bilirubin_indirect', 'total_protein', 'albumin', 'a_g_ratio',
    'globulin', 'cholesterol_total', 'triglycerides', 'hdl_cholesterol', 'ldl_cholesterol',
    'vldl_cholesterol', 'non_hdl_cholesterol', 'Carbohydrate', 'Fiber', 'Sugar', 'Fat',
    'Saturated Fat', 'Polyunsaturated Fat', 'Monounsaturated Fat', 'Trans Fat',
    'Cholesterol', 'Sodium', 'Potassium', 'Vitamin A', 'Calcium', 'Iron'
]

# Load your nutrient and blood data
print("Loading your nutrient and blood data...")
nutrient_data = pd.read_excel(NUTRIENT_FILE)
blood_data = pd.read_excel(BLOOD_FILE)

# Combine into one DataFrame (assuming 1 row per file for simplicity)
your_data_df = pd.concat([blood_data, nutrient_data], axis=1)

# Map your column names to expected feature names (case-insensitive, partial match)
column_mapping = {}
for expected in feature_names:
    for col in your_data_df.columns:
        if expected.lower() in col.lower():  # Flexible matching
            column_mapping[col] = expected
your_data_df = your_data_df.rename(columns=column_mapping)

# Reindex to match the 37 features, fill missing with synthetic data averages
synthetic_data = pd.read_csv('disease_dataset.csv')
averages = synthetic_data[feature_names].mean()
your_data_df = your_data_df.reindex(columns=feature_names).fillna(averages)

# Convert to NumPy array (first row only for now)
your_data = your_data_df.values[:1]  # Shape: (1, 37)
print("Your data loaded and formatted successfully!")

# Scale the data
your_data_scaled = scaler.transform(your_data)

# Predict
predictions = model.predict(your_data_scaled)
diseases = ['Diabetes', 'Hypertension', 'CKD', 'Liver Cirrhosis', 'Hyperlipidemia',
            'CAD', 'Gout', 'NAFLD', 'Osteoporosis', 'Metabolic Syndrome']

# Disease thresholds and modification rules
disease_rules = {
    'Diabetes': {'features': ['Sugar', 'triglycerides'], 'thresholds': [50, 150], 'reduce_by': [20, 50]},
    'Hypertension': {'features': ['Sodium', 'Potassium'], 'thresholds': [3000, 2000], 'reduce_by': [1000, -500]},
    'CKD': {'features': ['gfr_estimated', 'creatinine'], 'thresholds': [60, 1.5], 'reduce_by': [-30, 0.5]},
    'Liver Cirrhosis': {'features': ['ast', 'alt', 'bilirubin_total'], 'thresholds': [40, 40, 1.2], 'reduce_by': [15, 15, 0.5]},
    'Hyperlipidemia': {'features': ['cholesterol_total', 'triglycerides'], 'thresholds': [200, 150], 'reduce_by': [50, 50]},
    'CAD': {'features': ['non_hdl_cholesterol', 'Saturated Fat'], 'thresholds': [160, 20], 'reduce_by': [40, 10]},
    'Gout': {'features': ['uric_acid'], 'thresholds': [7], 'reduce_by': [2]},
    'NAFLD': {'features': ['alt', 'ggtp', 'Fat'], 'thresholds': [40, 50, 70], 'reduce_by': [15, 20, 30]},
    'Osteoporosis': {'features': ['Calcium'], 'thresholds': [600], 'reduce_by': [-200]},
    'Metabolic Syndrome': {'features': ['triglycerides', 'hdl_cholesterol', 'Sugar'], 'thresholds': [150, 40, 50], 'reduce_by': [50, -10, 20]}
}

# Print predictions and advice
print("\nDisease Predictions and Recommendations for Your Data:")
for i, disease in enumerate(diseases):
    prob = predictions[0][i]
    pred = 1 if prob > 0.5 else 0
    print(f"\n{disease}: Probability = {prob:.4f}, Prediction = {'Yes' if pred == 1 else 'No'}")
    
    if prob > 0.4:  # Suggest changes if risk is moderate to high
        rules = disease_rules[disease]
        print(f"  To reduce {disease} risk:")
        for feature, thresh, change in zip(rules['features'], rules['thresholds'], rules['reduce_by']):
            idx = feature_names.index(feature)
            current_value = your_data[0][idx]
            if (change > 0 and current_value > thresh) or (change < 0 and current_value < thresh):
                target_value = current_value - change
                direction = "reduce" if change > 0 else "increase"
                units = "g/day" if feature in ['Carbohydrate', 'Fiber', 'Sugar', 'Fat', 'Saturated Fat', 
                                              'Polyunsaturated Fat', 'Monounsaturated Fat', 'Trans Fat'] else \
                        "mg/day" if feature in ['Cholesterol', 'Sodium', 'Potassium', 'Vitamin A', 'Calcium', 'Iron'] else \
                        "mg/dL" if feature in ['triglycerides', 'hdl_cholesterol', 'ldl_cholesterol', 'vldl_cholesterol', 
                                              'non_hdl_cholesterol', 'cholesterol_total', 'creatinine', 'bilirubin_total', 
                                              'bilirubin_direct', 'bilirubin_indirect', 'uric_acid'] else \
                        "U/L" if feature in ['ast', 'alt', 'ggtp', 'alkaline_phosphatase'] else "units"
                print(f"    - {direction.capitalize()} {feature} from {current_value:.1f} to {target_value:.1f} {units}")