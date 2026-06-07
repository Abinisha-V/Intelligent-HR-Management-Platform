import pytest
import json
from app import db
from app import CandidateScreening, EmployeeRecord

class TestAPIEndpoints:
    """Test cases for REST API endpoints"""

    def test_resume_screen_api_valid_request(self, client, app):
        """Test resume screening API with valid data"""
        with app.app_context():
            # Create tables
            db.create_all()

            test_data = {
                "name": "John Doe",
                "email": "john@example.com",
                "job_description": "Python developer with Flask experience",
                "resume_text": "Experienced Python developer with Flask, Django, and machine learning skills"
            }

            response = client.post('/api/resume-screen',
                                 data=json.dumps(test_data),
                                 content_type='application/json')

            assert response.status_code == 201
            data = json.loads(response.data)

            assert "id" in data
            assert data["name"] == "John Doe"
            assert data["email"] == "john@example.com"
            assert "score" in data
            assert "status" in data
            assert isinstance(data["score"], (int, float))
            assert data["status"] in ["Shortlisted", "Maybe", "Rejected"]

    def test_resume_screen_api_missing_fields(self, client):
        """Test resume screening API with missing required fields"""
        incomplete_data = {
            "name": "John Doe",
            "email": "john@example.com"
            # Missing job_description and resume_text
        }

        response = client.post('/api/resume-screen',
                             data=json.dumps(incomplete_data),
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_performance_predict_api_valid_request(self, client, app):
        """Test performance prediction API with valid data"""
        with app.app_context():
            db.create_all()

            test_data = {
                "name": "Jane Smith",
                "role": "Developer",
                "tasks_completed": 45,
                "avg_completion_time": 2.1,
                "attendance": 95,
                "manager_rating": 4.8,
                "deadlines_missed": 0
            }

            response = client.post('/api/performance-predict',
                                 data=json.dumps(test_data),
                                 content_type='application/json')

            assert response.status_code == 201
            data = json.loads(response.data)

            assert "id" in data
            assert data["name"] == "Jane Smith"
            assert data["role"] == "Developer"
            assert "performance_prediction" in data
            assert "attrition_risk" in data
            assert "attrition_probability" in data
            assert data["performance_prediction"] in ["Low Performer", "Average Performer", "High Performer"]
            assert data["attrition_risk"] in ["Low", "High"]

    def test_performance_predict_api_invalid_data(self, client):
        """Test performance prediction API with invalid numeric data"""
        invalid_data = {
            "name": "Jane Smith",
            "role": "Developer",
            "tasks_completed": "not_a_number",
            "avg_completion_time": 2.1,
            "attendance": 95,
            "manager_rating": 4.8,
            "deadlines_missed": 0
        }

        response = client.post('/api/performance-predict',
                             data=json.dumps(invalid_data),
                             content_type='application/json')

        assert response.status_code == 500  # Should fail with conversion error

    def test_analytics_api(self, client, app):
        """Test analytics API endpoint"""
        with app.app_context():
            db.create_all()

            # Add some test data
            candidate = CandidateScreening(
                name="Test Candidate",
                email="test@example.com",
                job_description="Test job",
                resume_filename="test.pdf",
                score=85.0,
                status="Shortlisted"
            )
            db.session.add(candidate)

            employee = EmployeeRecord(
                name="Test Employee",
                role="Developer",
                tasks_completed=40,
                avg_completion_time=2.5,
                attendance=90,
                manager_rating=4.5,
                deadlines_missed=1,
                performance_prediction="High Performer",
                attrition_risk="Low",
                attrition_probability=0.2
            )
            db.session.add(employee)
            db.session.commit()

            response = client.get('/api/analytics')
            assert response.status_code == 200

            data = json.loads(response.data)
            assert "summary" in data
            assert "performance_distribution" in data
            assert "attrition_distribution" in data
            assert "recent_candidates" in data
            assert "recent_employees" in data

            assert data["summary"]["total_candidates"] >= 1
            assert data["summary"]["total_employees"] >= 1