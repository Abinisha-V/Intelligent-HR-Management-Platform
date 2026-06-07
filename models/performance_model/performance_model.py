# ------------------------------
# IMPORT REQUIRED LIBRARIES
# ------------------------------
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

MODEL_FILE = os.path.join(os.path.dirname(__file__), "saved_model.pkl")
DATA_FILE = os.path.join(os.path.dirname(__file__), "employee_data.csv")


def train_performance_model():
    """Train performance classification model and save to disk."""
    data = pd.read_csv(DATA_FILE)

    X = data[["tasks_completed", "avg_completion_time", "attendance", "manager_rating", "deadlines_missed"]]
    y = data["performance_label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Performance Model Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    joblib.dump(model, MODEL_FILE)
    return model


def load_performance_model():
    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    else:
        return train_performance_model()


def predict_performance(employee_data):
    """Predict performance label from numeric features list."""
    model = load_performance_model()
    prediction = model.predict([employee_data])[0]

    mapping = {0: "Low Performer", 1: "Average Performer", 2: "High Performer"}
    return mapping.get(prediction, "Unknown")


if __name__ == "__main__":
    print("Training performance model...")
    train_performance_model()

    print("Sample prediction:")
    sample = [40, 2.5, 90, 4.5, 1]
    print(predict_performance(sample))
