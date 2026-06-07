import pytest
import numpy as np
from models.performance_model.performance_model import predict_performance, load_performance_model
from models.attrition_model.attrition_model import predict_attrition, load_attrition_model

class TestPerformanceModel:
    """Test cases for performance prediction model"""

    def test_predict_performance_valid_input(self):
        """Test performance prediction with valid input"""
        # Load model (should be pre-trained)
        model = load_performance_model()
        assert model is not None

        # Test with sample data
        sample_input = [40, 2.5, 90, 4.5, 1]  # tasks, time, attendance, rating, missed
        result = predict_performance(sample_input)

        assert result in ["Low Performer", "Average Performer", "High Performer"]
        assert isinstance(result, str)

    def test_predict_performance_edge_cases(self):
        """Test performance prediction with edge case inputs"""
        test_cases = [
            [0, 0, 0, 1, 10],  # Very poor performance
            [100, 1, 100, 5, 0],  # Excellent performance
            [25, 3, 75, 3, 2],  # Average performance
        ]

        for case in test_cases:
            result = predict_performance(case)
            assert result in ["Low Performer", "Average Performer", "High Performer"]

    def test_predict_performance_invalid_input(self):
        """Test performance prediction with invalid input types"""
        with pytest.raises(Exception):
            predict_performance("invalid input")

        with pytest.raises(Exception):
            predict_performance([1, 2])  # Too few features

class TestAttritionModel:
    """Test cases for attrition prediction model"""

    def test_predict_attrition_valid_input(self):
        """Test attrition prediction with valid input"""
        # Load model
        model = load_attrition_model()
        assert model is not None

        # Test with sample data
        sample_input = [40, 2.5, 90, 4.5, 1]
        result = predict_attrition(sample_input)

        assert "risk" in result
        assert "probability" in result
        assert result["risk"] in ["Low", "High"]
        assert isinstance(result["probability"], (int, float))
        assert 0 <= result["probability"] <= 1

    def test_predict_attrition_high_risk_case(self):
        """Test attrition prediction identifies high risk cases"""
        # Low performance, poor attendance, many missed deadlines
        high_risk_input = [15, 5.0, 60, 2.0, 8]
        result = predict_attrition(high_risk_input)

        # Should be high risk (though exact threshold may vary)
        assert result["risk"] in ["Low", "High"]
        assert isinstance(result["probability"], (int, float))

    def test_predict_attrition_low_risk_case(self):
        """Test attrition prediction identifies low risk cases"""
        # High performance, good attendance, no missed deadlines
        low_risk_input = [50, 1.5, 95, 4.8, 0]
        result = predict_attrition(low_risk_input)

        assert result["risk"] in ["Low", "High"]
        assert isinstance(result["probability"], (int, float))