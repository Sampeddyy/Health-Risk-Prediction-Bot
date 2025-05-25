import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

# Step 1: Load the synthetic dataset
print("Loading dataset...")
df = pd.read_csv('disease_dataset.csv')  # Ensure this file is in your working directory
print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# Step 2: Prepare features (X) and labels (y)
X = df.drop(columns=['Diabetes', 'Hypertension', 'CKD', 'Liver Cirrhosis', 
                     'Hyperlipidemia', 'CAD', 'Gout', 'NAFLD', 'Osteoporosis', 
                     'Metabolic Syndrome']).values
y = df[['Diabetes', 'Hypertension', 'CKD', 'Liver Cirrhosis', 'Hyperlipidemia', 
        'CAD', 'Gout', 'NAFLD', 'Osteoporosis', 'Metabolic Syndrome']].values
print(f"Features shape: {X.shape}, Labels shape: {y.shape}")

# Step 3: Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Features scaled successfully.")

# Step 4: Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Test set: {X_test.shape[0]} rows")

# Step 5: Build the TensorFlow neural network
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),  # Explicit Input layer
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.summary()

# Step 6: Train the model
print("Training TensorFlow model...")
history = model.fit(X_train, y_train, 
                    epochs=30,          # Increased epochs for better convergence
                    batch_size=32, 
                    validation_split=0.2, 
                    verbose=1)
print("Model training completed!")

# Step 7: Evaluate the model
print("Evaluating model performance...")
y_pred_probs = model.predict(X_test)
y_pred = (y_pred_probs > 0.5).astype(int)  # Threshold at 0.5

# Accuracy per disease
print("\nAccuracy per disease:")
for i, disease in enumerate(['Diabetes', 'Hypertension', 'CKD', 'Liver Cirrhosis', 
                             'Hyperlipidemia', 'CAD', 'Gout', 'NAFLD', 'Osteoporosis', 
                             'Metabolic Syndrome']):
    acc = np.mean(y_test[:, i] == y_pred[:, i])
    print(f"{disease}: {acc:.4f}")

# Overall accuracy (all labels correct)
overall_acc = np.mean((y_test == y_pred).all(axis=1))
print(f"\nOverall Accuracy (all labels correct): {overall_acc:.4f}")

# Step 8: Save the model and scaler
print("Saving model and scaler...")
model.save('disease_model_tf.keras') # Fixed with .keras extension
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("Model saved as 'disease_model_tf.keras', scaler as 'scaler.pkl'")

# Step 9: Optional - Plot training history
import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()
plt.show()