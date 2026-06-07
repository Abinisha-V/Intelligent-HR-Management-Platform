import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "../performance_model/employee_data.csv")
MODEL_FILE = os.path.join(BASE_DIR, "saved_attrition_model.pkl")


def _create_attrition_label(df):
    # synthetic attrition logic: low performance, low attendance, high deadlines missed
    attrition = ((df["performance_label"] == 0) | (df["attendance"] < 80) | (df["deadlines_missed"] > 3)).astype(int)
    return attrition


def train_attrition_model():
    df = pd.read_csv(DATA_FILE)
    df["attrition"] = _create_attrition_label(df)

    features = ["tasks_completed", "avg_completion_time", "attendance", "manager_rating", "deadlines_missed"]
    X = df[features]
    y = df["attrition"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Attrition Model Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    joblib.dump(model, MODEL_FILE)
    return model


def load_attrition_model():
    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    else:
        return train_attrition_model()


def predict_attrition(employee_data):
    model = load_attrition_model()
    probability = model.predict_proba([employee_data])[0][1]
    risk = "High" if probability >= 0.5 else "Low"
    return {
        "risk": risk,
        "probability": round(float(probability), 4)
    }


if __name__ == "__main__":
    print("Training attrition model...")
    train_attrition_model()
