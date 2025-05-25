import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of rows
n_rows = 15000

# Blood parameters (clinical ranges)
blood_data = {
    'creatinine': np.random.uniform(0.6, 2.5, n_rows),
    'gfr_estimated': np.random.uniform(20, 120, n_rows),
    'urea': np.random.uniform(10, 60, n_rows),
    'urea_nitrogen_blood': np.random.uniform(5, 30, n_rows),
    'bun_creatinine_ratio': np.random.uniform(10, 25, n_rows),
    'uric_acid': np.random.uniform(3, 10, n_rows),
    'ast': np.random.uniform(10, 100, n_rows),
    'alt': np.random.uniform(10, 100, n_rows),
    'ggtp': np.random.uniform(10, 80, n_rows),
    'alkaline_phosphatase': np.random.uniform(30, 120, n_rows),
    'bilirubin_total': np.random.uniform(0.1, 2.0, n_rows),
    'bilirubin_direct': np.random.uniform(0.0, 0.5, n_rows),
    'bilirubin_indirect': np.random.uniform(0.1, 1.5, n_rows),
    'total_protein': np.random.uniform(6, 8, n_rows),
    'albumin': np.random.uniform(3.5, 5.5, n_rows),
    'a_g_ratio': np.random.uniform(1.0, 2.5, n_rows),
    'globulin': np.random.uniform(2.0, 3.5, n_rows),
    'cholesterol_total': np.random.uniform(120, 300, n_rows),
    'triglycerides': np.random.uniform(50, 250, n_rows),
    'hdl_cholesterol': np.random.uniform(30, 80, n_rows),
    'ldl_cholesterol': np.random.uniform(50, 200, n_rows),
    'vldl_cholesterol': np.random.uniform(10, 50, n_rows),
    'non_hdl_cholesterol': np.random.uniform(80, 250, n_rows),
}

# Nutrient intake (dietary ranges)
nutrient_data = {
    'Carbohydrate': np.random.uniform(100, 400, n_rows),
    'Fiber': np.random.uniform(10, 40, n_rows),
    'Sugar': np.random.uniform(20, 100, n_rows),
    'Fat': np.random.uniform(20, 100, n_rows),
    'Saturated Fat': np.random.uniform(5, 30, n_rows),
    'Polyunsaturated Fat': np.random.uniform(5, 20, n_rows),
    'Monounsaturated Fat': np.random.uniform(5, 30, n_rows),
    'Trans Fat': np.random.uniform(0, 5, n_rows),
    'Cholesterol': np.random.uniform(100, 400, n_rows),
    'Sodium': np.random.uniform(1500, 4500, n_rows),
    'Potassium': np.random.uniform(1500, 4000, n_rows),
    'Vitamin A': np.random.uniform(500, 2000, n_rows),
    'Calcium': np.random.uniform(500, 1500, n_rows),
    'Iron': np.random.uniform(5, 20, n_rows),
}

# Combine into DataFrame
df = pd.DataFrame({**blood_data, **nutrient_data})

# Probabilistic disease rules with gradients and nutrient weighting
def sigmoid_prob(x, threshold, steepness=0.1):
    return 1 / (1 + np.exp(-(x - threshold) / steepness))

# Diabetes: 50% nutrients, 50% blood
df['Diabetes'] = (0.5 * sigmoid_prob(df['Sugar'], 50) + 
                  0.5 * sigmoid_prob(df['triglycerides'], 150) > 0.7).astype(int)

# Hypertension: 40% nutrients, 60% balance
df['Hypertension'] = (0.4 * sigmoid_prob(df['Sodium'], 3000) + 
                      0.4 * sigmoid_prob(df['Potassium'], 2000, steepness=-0.1) > 0.6).astype(int)

# CKD: 70% blood, 30% indirect
df['CKD'] = (0.5 * sigmoid_prob(df['gfr_estimated'], 60, steepness=-0.1) + 
             0.5 * sigmoid_prob(df['creatinine'], 1.5) > 0.7).astype(int)

# Liver Cirrhosis: 80% blood, 20% nutrients
df['Liver Cirrhosis'] = (0.3 * sigmoid_prob(df['ast'], 40) + 
                         0.3 * sigmoid_prob(df['alt'], 40) + 
                         0.2 * sigmoid_prob(df['bilirubin_total'], 1.2) > 0.6).astype(int)

# Hyperlipidemia: 70% blood, 30% nutrients
df['Hyperlipidemia'] = (0.5 * sigmoid_prob(df['cholesterol_total'], 200) + 
                        0.5 * sigmoid_prob(df['triglycerides'], 150) > 0.7).astype(int)

# CAD: 50% blood, 50% nutrients
df['CAD'] = (0.5 * sigmoid_prob(df['non_hdl_cholesterol'], 160) + 
             0.5 * sigmoid_prob(df['Saturated Fat'], 20) > 0.7).astype(int)

# Gout: 90% blood, 10% indirect
df['Gout'] = (sigmoid_prob(df['uric_acid'], 7) > 0.6).astype(int)

# NAFLD: 60% blood, 40% nutrients
df['NAFLD'] = (0.3 * sigmoid_prob(df['alt'], 40) + 
               0.3 * sigmoid_prob(df['ggtp'], 50) + 
               0.4 * sigmoid_prob(df['Fat'], 70) > 0.7).astype(int)

# Osteoporosis: 80% nutrients, 20% indirect
df['Osteoporosis'] = (sigmoid_prob(df['Calcium'], 600, steepness=-0.1) > 0.6).astype(int)

# Metabolic Syndrome: 60% blood, 40% nutrients
df['Metabolic Syndrome'] = (0.4 * sigmoid_prob(df['triglycerides'], 150) + 
                            0.3 * sigmoid_prob(df['hdl_cholesterol'], 40, steepness=-0.1) + 
                            0.3 * sigmoid_prob(df['Sugar'], 50) > 0.7).astype(int)

# Add comorbidity noise (controlled randomness)
rng = np.random.RandomState(42)
df.loc[df['Diabetes'] == 1, 'CAD'] = rng.choice([0, 1], size=sum(df['Diabetes'] == 1), p=[0.4, 0.6])
df.loc[df['Hyperlipidemia'] == 1, 'CAD'] = rng.choice([0, 1], size=sum(df['Hyperlipidemia'] == 1), p=[0.5, 0.5])
df.loc[df['CKD'] == 1, 'Hypertension'] = rng.choice([0, 1], size=sum(df['CKD'] == 1), p=[0.3, 0.7])

# Save to Excel (per flow list)
df.to_excel('training_data.xlsx', index=False)
print("Dataset generated and saved as 'training_data.xlsx'!")
