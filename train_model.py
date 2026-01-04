# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load the dataset
df = pd.read_csv('Crop_recommendation_updated.csv')

# Features and target
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']  # 'label' is the crop/disease column

# ✅ Print dataset info
print(f"✅ Total Samples: {len(df)}")
print(f"✅ Unique Crops: {y.nunique()}")
print("\n✅ Crop Sample Counts:\n")
print(y.value_counts())

# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Model Accuracy: {accuracy * 100:.2f}%")

# Save model
with open('crop_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("✅ Model trained and saved as crop_model.pkl")
