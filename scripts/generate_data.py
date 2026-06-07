#!/usr/bin/env python3
"""
HR AI System - Sample Data Generator
Generates synthetic employee data for testing and training
"""

import pandas as pd
import numpy as np
import os

def generate_employee_data(num_samples=100):
    """Generate synthetic employee performance data"""

    np.random.seed(42)

    data = []

    for i in range(num_samples):
        # Generate realistic employee metrics
        tasks_completed = np.random.normal(35, 10)  # Mean 35, std 10
        tasks_completed = max(0, min(100, tasks_completed))  # Clamp between 0-100

        avg_completion_time = np.random.normal(3.0, 1.0)  # Mean 3.0 hours, std 1.0
        avg_completion_time = max(0.5, min(8.0, avg_completion_time))  # Clamp

        attendance = np.random.normal(85, 15)  # Mean 85%, std 15
        attendance = max(0, min(100, attendance))  # Clamp

        manager_rating = np.random.normal(3.5, 1.0)  # Mean 3.5, std 1.0
        manager_rating = max(1.0, min(5.0, manager_rating))  # Clamp

        deadlines_missed = np.random.poisson(2)  # Poisson distribution
        deadlines_missed = max(0, min(10, deadlines_missed))  # Clamp

        # Determine performance label based on metrics
        score = (
            (tasks_completed / 50) * 0.3 +  # 30% weight on tasks
            ((8 - avg_completion_time) / 7) * 0.2 +  # 20% weight on time (lower is better)
            (attendance / 100) * 0.25 +  # 25% weight on attendance
            (manager_rating / 5) * 0.15 +  # 15% weight on rating
            ((10 - deadlines_missed) / 10) * 0.1  # 10% weight on deadlines (lower is better)
        ) * 100

        if score >= 75:
            performance_label = 2  # High Performer
        elif score >= 50:
            performance_label = 1  # Average Performer
        else:
            performance_label = 0  # Low Performer

        data.append({
            'tasks_completed': round(tasks_completed, 1),
            'avg_completion_time': round(avg_completion_time, 1),
            'attendance': round(attendance, 1),
            'manager_rating': round(manager_rating, 1),
            'deadlines_missed': deadlines_missed,
            'performance_label': performance_label
        })

    return pd.DataFrame(data)

def generate_sample_resumes(num_samples=10):
    """Generate sample resume texts for testing"""

    job_descriptions = [
        "Python developer with Flask, Django, and machine learning experience",
        "Data scientist proficient in pandas, scikit-learn, and SQL",
        "Full-stack developer with React, Node.js, and PostgreSQL",
        "DevOps engineer with AWS, Docker, and Kubernetes expertise",
        "Frontend developer specializing in Vue.js and TypeScript"
    ]

    resumes = [
        "Experienced Python developer with 5 years of experience in Flask, Django, and machine learning. Proficient in pandas, numpy, and scikit-learn. Strong background in SQL and data analysis.",
        "Data scientist with expertise in machine learning algorithms, statistical analysis, and data visualization. Skilled in Python, R, SQL, and Tableau. Experience with large datasets and predictive modeling.",
        "Full-stack developer with 4 years of experience in React, Node.js, Express, and MongoDB. Knowledge of REST APIs, GraphQL, and modern JavaScript frameworks. Experience with agile development.",
        "DevOps engineer specializing in AWS cloud infrastructure, Docker containers, and CI/CD pipelines. Experience with Kubernetes, Terraform, and monitoring tools like Prometheus and Grafana.",
        "Frontend developer with expertise in Vue.js, TypeScript, and modern CSS frameworks. Experience with state management, testing, and performance optimization. Knowledge of UX/UI principles.",
        "Software engineer with background in Java, Spring Boot, and microservices architecture. Experience with cloud platforms and containerization technologies.",
        "AI/ML engineer focused on natural language processing and computer vision. Proficient in TensorFlow, PyTorch, and deep learning frameworks.",
        "Database administrator with expertise in PostgreSQL, MySQL, and MongoDB. Experience with database design, optimization, and backup strategies.",
        "Mobile app developer specializing in React Native and Flutter. Experience with iOS and Android development, app store deployment, and cross-platform solutions.",
        "Security engineer with knowledge of cybersecurity principles, penetration testing, and secure coding practices. Experience with tools like OWASP and vulnerability assessment."
    ]

    return job_descriptions[:num_samples], resumes[:num_samples]

def main():
    print("Generating Sample Data for HR AI System...")

    # Create directories if they don't exist
    os.makedirs("models/performance_model", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Generate employee performance data
    print("[INFO] Generating employee performance data...")
    employee_df = generate_employee_data(200)
    employee_df.to_csv("models/performance_model/employee_data.csv", index=False)
    print(f"[SUCCESS] Generated {len(employee_df)} employee records")

    # Generate sample resumes
    print("[INFO] Generating sample resume data...")
    job_descs, resumes = generate_sample_resumes(10)

    sample_data = []
    for i, (job_desc, resume) in enumerate(zip(job_descs, resumes)):
        sample_data.append({
            'job_description': job_desc,
            'resume_text': resume,
            'expected_score': 85 - (i * 5)  # Decreasing scores for variety
        })

    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv("data/sample_resumes.csv", index=False)
    print(f"[SUCCESS] Generated {len(sample_df)} sample resume pairs")

    # Print statistics
    print("\n[INFO] Data Statistics:")
    print(f"Performance labels distribution:")
    print(employee_df['performance_label'].value_counts().sort_index())

    print("[INFO] Files created:")
    print("   - models/performance_model/employee_data.csv")
    print("   - data/sample_resumes.csv")

    print("\nSample data generation complete!")

if __name__ == "__main__":
    main()