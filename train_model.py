import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("Untitled spreadsheet - Sheet1.csv")

print("Dataset loaded successfully")
print(data.head())

# Encode categorical columns

le_consciousness = LabelEncoder()
data["consciousness"] = le_consciousness.fit_transform(data["consciousness"])

le_symptoms = LabelEncoder()
data["symptoms"] = le_symptoms.fit_transform(data["symptoms"])

# Separate features and target

X = data.drop("triage_priority", axis=1)
y = data["triage_priority"]

# Split dataset into training and testing

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create Decision Tree model

model = DecisionTreeClassifier()

# Train model

model.fit(X_train, y_train)

print("Model training completed")

# Make predictions

predictions = model.predict(X_test)

# Calculate accuracy

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", accuracy)

# Confusion Matrix

cm = confusion_matrix(y_test, predictions)

print("\nConfusion Matrix:")
print(cm)

# Classification Report

report = classification_report(y_test, predictions)

print("\nClassification Report:")
print(report)

# Save trained model

joblib.dump(model, "triage_model.pkl")

print("\nModel saved as triage_model.pkl")

# Visualize Decision Tree

plt.figure(figsize=(20,10))

plot_tree(
    model,
    feature_names=X.columns,
    class_names=["Critical","High","Medium","Low"],
    filled=True
)

plt.title("Decision Tree for Medical Triage Prediction")

plt.savefig("decision_tree.png")

plt.show()