import pandas as pd
from pathlib import Path


# Find the MentorMatch project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Find the data folder
DATA_DIR = BASE_DIR / "data"

# Load our generated training dataset
data = pd.read_csv(DATA_DIR / "match_training_data.csv")

print(data.head())
# Separate features and target

X = data[
    [
        "skill_overlap",
        "career_goal_match",
        "industry_match",
        "interest_match",
        "experience_fit",
        "availability_match"
    ]
]

y = data["good_match"]

print("\nFeatures (X):")
print(X.head())

print("\nTarget (y):")
print(y.head())
from sklearn.model_selection import train_test_split


# Split data into training and testing sets

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))
from sklearn.ensemble import RandomForestClassifier


# Create the model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)


# Train the model
model.fit(X_train, y_train)

print("\nModel trained successfully!")
# Make predictions on the test data

y_pred = model.predict(X_test)

print("\nPredictions:")
print(y_pred[:20])
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# Evaluate the model

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\nModel Evaluation:")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
# Save the trained model

import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(exist_ok=True)

joblib.dump(model, MODEL_DIR / "mentor_model.pkl")

print("\nModel saved successfully!")