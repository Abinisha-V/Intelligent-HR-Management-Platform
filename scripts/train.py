#!/usr/bin/env python3
"""
HR AI System - Model Training Script
Retrains all ML models with current data
"""

import os
import sys
import pandas as pd

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.performance_model.performance_model import train_performance_model
from models.attrition_model.attrition_model import train_attrition_model

def main():
    print("Starting HR AI Model Training...")

    try:
        # Check if data files exist
        perf_data = "models/performance_model/employee_data.csv"
        if not os.path.exists(perf_data):
            print(f"[ERROR] Performance data file not found: {perf_data}")
            return 1

        print("[INFO] Training Performance Model...")
        train_performance_model()

        print("[INFO] Training Attrition Model...")
        train_attrition_model()

        print("[SUCCESS] All models trained successfully!")
        print("[INFO] Model files saved:")
        print("   - models/performance_model/saved_model.pkl")
        print("   - models/attrition_model/saved_attrition_model.pkl")

        return 0

    except Exception as e:
        print(f"[ERROR] Training failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())