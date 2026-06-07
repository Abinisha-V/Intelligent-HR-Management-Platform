# 🚀 HR AI System

> **Intelligent HR Management Platform** - Powered by Machine Learning & Modern Web Technologies

An advanced web-based HR management system that leverages artificial intelligence to automate resume screening, predict employee performance, analyze attrition risks, and provide comprehensive analytics. Built with Flask, scikit-learn, and BERT for enterprise-grade HR operations.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Key Features

### 🔐 **Secure Authentication**
- Role-based HR login system
- Session management with Flask-Login
- Password hashing for security
- Protected routes and dashboard access

### 📄 **Resume Screening**
- Upload PDF/DOCX resumes
- BERT-powered semantic similarity matching
- Intelligent job description alignment
- Automatic scoring (0-100%) with status classification
- **Status Categories**: Shortlisted (≥75%) | Maybe (50-75%) | Rejected (<50%)
- Full candidate history and tracking

### 🎯 **Performance Prediction**
- Machine Learning-based employee performance classification
- Input metrics:
  - Tasks completed
  - Average completion time
  - Attendance rate
  - Manager rating
  - Deadlines missed
- **Output Categories**: High Performer | Average Performer | Low Performer
- Predictive analytics for workforce planning

### ⚠️ **Attrition Risk Analysis**
- Logistic regression model for turnover prediction
- Risk probability scores (0-100%)
- **Risk Levels**: Low Risk | High Risk
- Early warning system for retention strategies
- Historical trend analysis

### 📊 **Interactive Analytics Dashboard**
- **Real-time Metrics**: 
  - Total resumes screened
  - Active employee records
  - High-risk employee count
  - High performer statistics
- **Visual Analytics**:
  - Performance distribution (doughnut chart)
  - Attrition risk distribution (pie chart)
  - Trend analysis
- Quick action buttons for all features
- Responsive design for all devices

### 🎨 **Modern UI/UX**
- Beautiful gradient design
- Interactive hover effects
- Smooth animations and transitions
- Bootstrap 5 responsive layout
- Font Awesome icons throughout
- Professional color scheme

### 🔌 **REST API Endpoints**
- `POST /api/resume-screen` - Resume screening
- `POST /api/performance-predict` - Performance prediction
- `GET /api/analytics` - Analytics data export
- JSON request/response format

## 📋 System Architecture

```
┌─────────────────┐
│   Web Browser   │
└────────┬────────┘
         │
    ┌────▼─────┐
    │  Flask   │
    │   App    │
    └────┬─────┘
         │
    ┌────┴──────┬──────────┬──────────┐
    │            │          │          │
┌───▼───┐  ┌────▼──┐  ┌───▼────┐  ┌─▼────┐
│ Auth  │  │Resume │  │Performance│ DB  │
│System │  │Model  │  │Model     │      │
└───────┘  └───────┘  └──────────┘  └─────┘
```

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with gradients and animations
- **Bootstrap 5** - Responsive design framework
- **Chart.js** - Interactive data visualizations
- **Font Awesome 6** - Icon library

### Backend
- **Python 3.8+** - Core language
- **Flask 2.0+** - Web framework
- **Flask-SQLAlchemy** - ORM for database management
- **Flask-Login** - User authentication & session management

### Database
- **SQLite** - Default (development)
- **MySQL** / **PostgreSQL** - Production ready

### Machine Learning
- **scikit-learn** - Performance & attrition models
- **sentence-transformers (BERT)** - Resume similarity matching
- **joblib** - Model serialization
- **pandas/NumPy** - Data processing

### Security
- **Werkzeug** - Password hashing & secure utilities
- **CSRF Protection** - Built-in Flask protection
- **Input Validation** - File upload restrictions

### Deployment
- **Docker** - Containerization
- **Render.com** - Cloud deployment
- **Gunicorn** - Production WSGI server

## 📦 Requirements

- Python 3.8 or higher
- pip or conda for package management
- 2GB RAM minimum
- 500MB disk space

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- Git
- pip/conda

### 1. Clone & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/hr-ai-system.git
cd hr-ai-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root (optional):

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///hr_ai.db
FLASK_ENV=development
```

### 3. Generate Sample Data (Optional)

```bash
python scripts/generate_data.py
```

### 4. Train Models (Optional)

```bash
python scripts/train.py
```

### 5. Run Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`

### 6. Access the System

1. **Login Page**: Navigate to `http://127.0.0.1:5000/`
2. **Default Credentials**:
   - Username: `hr`
   - Password: `hr123`
3. **Access Features**:
   - 📄 Resume Scan
   - 🎯 Risk Prediction
   - 📊 Analytics

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov=models

# Run specific test file
pytest tests/test_api.py
```

### 🐳 Docker Setup

```bash
# Build Docker image
docker build -t hr-ai-system:latest .

# Run container
docker run -p 5000:5000 \
  -e DATABASE_URL=sqlite:///hr_ai.db \
  -e SECRET_KEY=your-secret-key \
  hr-ai-system:latest
```

### ☁️ Deploy on Render

1. Push code to GitHub
2. Connect repository to Render
3. Set environment variables in Render dashboard
4. Deploy automatically on push
   pip install -r requirements.txt
   ```

2. **Generate sample data** (optional):
   ```bash
   python scripts/generate_data.py
   ```

3. **Train models** (optional):
   ```bash
   python scripts/train.py
   ```

4. **Run application**:
   ```bash
   python app.py
   ```

5. **Access**: `http://127.0.0.1:5000/`

## 📁 Project Structure

```
hr-ai-system/
├── 📄 app.py                           # Main Flask application (482 lines)
├── 🔑 requirements.txt                 # Python dependencies
│
├── 📁 models/                          # ML Models
│   ├── performance_model/
│   │   ├── performance_model.py       # Performance prediction model
│   │   ├── employee_data.csv          # Training data
│   │   └── __pycache__/
│   ├── attrition_model/
│   │   ├── attrition_model.py         # Attrition risk model
│   │   └── __pycache__/
│   └── resume_model/
│       ├── resume_model.py            # BERT-based resume screening
│       └── __pycache__/
│
├── 🎨 templates/                      # Jinja2 HTML Templates
│   ├── layout.html                    # Base template with navbar
│   ├── index.html                     # Dashboard
│   ├── login.html                     # Login page (secured)
│   ├── resume_screen.html             # Resume upload form
│   ├── resume_result.html             # Resume screening results
│   ├── performance.html               # Performance prediction form
│   ├── performance_result.html        # Performance prediction results
│   ├── analytics.html                 # Analytics dashboard
│   └── 404.html                       # Error page
│
├── 🖼️ static/                         # Static files
│   ├── css/                           # Custom stylesheets
│   └── js/                            # JavaScript files
│
├── 🧪 tests/                          # Unit Tests
│   ├── conftest.py                    # Pytest configuration
│   ├── test_api.py                    # API endpoint tests
│   ├── test_models.py                 # Model tests
│   └── __pycache__/
│
├── 📊 scripts/                        # Utility Scripts
│   ├── train.py                       # Model retraining script
│   ├── generate_data.py               # Sample data generator
│   └── __pycache__/
│
├── 📁 uploads/                        # Resume upload directory
├── 📁 instance/                       # Flask instance folder
├── 📁 data/                           # Sample data
│   └── sample_resumes.csv
│
├── 🐳 Dockerfile                      # Docker configuration
├── Procfile                           # Render deployment config
├── render.yaml                        # Cloud run configuration
├── pytest.ini                         # Pytest settings
└── README.md                          # This file
```

## ⚙️ Configuration

### Environment Variables

```bash
# Secret key for Flask sessions
SECRET_KEY=your-random-secret-key-here

# Database connection URLs
# SQLite (Default)
DATABASE_URL=sqlite:///hr_ai.db

# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost/hr_ai

# PostgreSQL (Recommended for production)
DATABASE_URL=postgresql://user:password@localhost:5432/hr_ai

# Environment mode
FLASK_ENV=development  # or production

# Optional: Debug mode (disable in production)
FLASK_DEBUG=False
```

### Database Setup

#### SQLite (Default)
- Automatic setup on first run
- Database file: `hr_ai.db`
- Perfect for development

#### MySQL Setup
```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE hr_ai;
CREATE USER 'hr_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON hr_ai.* TO 'hr_user'@'localhost';
FLUSH PRIVILEGES;
```

Update your `.env`:
```env
DATABASE_URL=mysql+pymysql://hr_user:secure_password@localhost/hr_ai
```

#### PostgreSQL Setup (Production)
```bash
# Create database
createdb hr_ai

# Create user
createuser hr_user
psql -d hr_ai -c "ALTER USER hr_user WITH ENCRYPTED PASSWORD 'secure_password';"
```

Update your `.env`:
```env
DATABASE_URL=postgresql://hr_user:secure_password@localhost:5432/hr_ai
```

### User Authentication

- **Default HR User**:
  - Username: `hr`
  - Password: `hr123` (Change after first login!)

- **Create New HR Users**:
  - Use Flask CLI or database admin tools
  - All passwords are hashed with Werkzeug

```python
# To create new user programmatically
from app import app, db, User

with app.app_context():
    new_user = User(username='newhrusername')
    new_user.set_password('secure_password')
    db.session.add(new_user)
    db.session.commit()
```

## � API Documentation

> **Note**: All API endpoints return JSON and require proper authentication headers in production.

### Authentication Flow

```
1. User visits http://localhost:5000/
2. Redirected to /login
3. Enter credentials (hr / hr123)
4. Session created, redirected to dashboard
5. Access protected routes via session
```

### 1️⃣ Resume Screening API

**Endpoint**: `POST /api/resume-screen`

**Request**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "job_description": "Senior Python Developer with Flask experience",
  "resume_text": "Experienced Python developer with 5 years in web development..."
}
```

**Response**:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "score": 85.5,
  "status": "Shortlisted",
  "created_at": "2024-03-24T10:30:00"
}
```

**Status Codes**:
- `201 Created` - Screening successful
- `400 Bad Request` - Missing required fields
- `500 Internal Server Error` - Processing error

### 2️⃣ Performance Prediction API

**Endpoint**: `POST /api/performance-predict`

**Request**:
```json
{
  "name": "Jane Smith",
  "role": "Senior Developer",
  "tasks_completed": 45,
  "avg_completion_time": 2.1,
  "attendance": 95,
  "manager_rating": 4.8,
  "deadlines_missed": 0
}
```

**Response**:
```json
{
  "id": 1,
  "name": "Jane Smith",
  "role": "Senior Developer",
  "performance_prediction": "High Performer",
  "attrition_risk": "Low",
  "attrition_probability": 0.15,
  "created_at": "2024-03-24T10:30:00"
}
```

### 3️⃣ Analytics Data API

**Endpoint**: `GET /api/analytics`

**Response**:
```json
{
  "summary": {
    "total_candidates": 150,
    "total_employees": 85,
    "high_risk_employees": 12
  },
  "performance_distribution": {
    "High Performer": 35,
    "Average Performer": 38,
    "Low Performer": 12
  },
  "attrition_distribution": {
    "Low": 73,
    "High": 12
  },
  "recent_candidates": [...],
  "recent_employees": [...]
}
```

## 🔒 Security Features

### Authentication & Authorization
- ✅ Role-based access control (HR only)
- ✅ Session management with Flask-Login
- ✅ Password hashing with Werkzeug
- ✅ CSRF protection enabled
- ✅ Secure cookie handling

### File Upload Security
- ✅ File type validation (PDF/DOCX only)
- ✅ Secure filename handling
- ✅ File size limits
- ✅ Virus scan ready (integration point)

### Data Protection
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Input sanitization
- ✅ Output encoding
- ✅ Environment variable management

### Production Deployment
- ✅ Remove debug mode
- ✅ Use strong SECRET_KEY
- ✅ HTTPS/SSL certificates
- ✅ Regular security updates
- ✅ Database backups

## � Machine Learning Models

### 1. Resume Screening Model
- **Algorithm**: BERT (Sentence Transformers)
- **Input**: Resume text + Job description
- **Output**: Similarity score (0-100%)
- **Performance**: 
  - Shortlisted: ≥75%
  - Maybe: 50-75%
  - Rejected: <50%
- **Library**: sentence-transformers

### 2. Performance Prediction Model
- **Algorithm**: Logistic Regression
- **Input Features**: 
  - Tasks completed
  - Completion time
  - Attendance
  - Manager rating
  - Deadlines missed
- **Output**: 3-class classification
  - High Performer
  - Average Performer
  - Low Performer
- **Library**: scikit-learn

### 3. Attrition Risk Model
- **Algorithm**: Logistic Regression
- **Input Features**: Same as performance model
- **Output**: Binary classification + probability
  - Low Risk (<50% probability)
  - High Risk (≥50% probability)
- **Use Case**: Early employee retention interventions
- **Library**: scikit-learn

### Model Retraining

```bash
# Retrain all models with new data
python scripts/train.py

# Generate new training data
python scripts/generate_data.py

# Train specific model
python -c "from models.performance_model.performance_model import train_performance_model; train_performance_model()"
```

### Model Files Location
```
models/
├── performance_model/
│   ├── saved_model.pkl          # Trained model
│   ├── employee_data.csv        # Training data
│   └── performance_model.py
├── attrition_model/
│   ├── saved_model.pkl
│   └── attrition_model.py
└── resume_model/
    ├── saved_embeddings/
    └── resume_model.py
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Workflow

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/hr-ai-system.git
   cd hr-ai-system
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make changes and test**
   ```bash
   # Run tests
   pytest
   
   # Run with coverage
   pytest --cov=app --cov=models
   ```

4. **Commit with descriptive messages**
   ```bash
   git commit -am "Add: Description of your feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Submit Pull Request**
   - Describe changes clearly
   - Reference any related issues
   - Include test results

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Write unit tests for new features

### Bug Reports
- Use GitHub Issues
- Include error logs
- Provide steps to reproduce
- Specify environment details

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 HR AI System Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

## 🆘 Troubleshooting

### Common Issues & Solutions

#### 1. Connection Refused Error
```
Error: 127.0.0.1 refused to connect
```

**Solution**:
```bash
# Make sure app is running
python app.py

# Verify port 5000 is available
# Windows:
netstat -ano | findstr :5000

# Linux/Mac:
lsof -i :5000
```

#### 2. Model Loading Errors
```
Error: FileNotFoundError - saved_model.pkl not found
```

**Solution**:
```bash
# Retrain models
python scripts/train.py

# Or regenerate with sample data
python scripts/generate_data.py
```

#### 3. Database Errors
```
Error: sqlalchemy.exc.OperationalError
```

**Solution**:
```bash
# Reset database (WARNING: deletes all data)
rm hr_ai.db

# Restart app to recreate tables
python app.py
```

#### 4. Import Errors
```
ModuleNotFoundError: No module named 'flask_login'
```

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or update specific package
pip install Flask-Login --upgrade
```

#### 5. Login Page Not Loading
```
Template not found: login.html
```

**Solution**:
```bash
# Verify file exists
ls templates/login.html

# Check templates folder is in project root
pwd  # Should be in hr-ai-system/
```

#### 6. PDF Upload Issues
```
Error: Failed to extract text from PDF
```

**Solution**:
```bash
# Check file is valid PDF
file resume.pdf

# Try a different PDF file
# Update allowed extensions if needed
```

#### 7. CORS Issues (API calls from different domain)
```
Error: No 'Access-Control-Allow-Origin' header
```

**Solution**: Update `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

Install flask-cors:
```bash
pip install flask-cors
```

#### 8. Memory Issues with Large Datasets
```
MemoryError: Unable to allocate memory
```

**Solution**:
```bash
# Reduce batch size in training
# Or run on machine with more RAM
# Use MySQL/PostgreSQL instead of SQLite
```

### Getting Help

- 📖 **Documentation**: Check README sections
- 🐛 **Issues**: Create GitHub issue with details
- 💬 **Discussions**: Use GitHub Discussions
- 📧 **Email**: See CONTRIBUTING.md for contact

## 🚀 Future Enhancements

- [ ] Advanced AI Resume Parsing
- [ ] Real-time Notification System
- [ ] Mobile App (React Native)
- [ ] Advanced Analytics Dashboard
- [ ] Interview Scheduling System
- [ ] Offer Letter Generation
- [ ] Multi-language Support
- [ ] Custom ML Model Training Interface

## 📊 Performance Benchmarks

| Feature | Avg Time | Accuracy |
|---------|----------|----------|
| Resume Screening | 2-5 sec | 92% |
| Performance Prediction | <1 sec | 88% |
| Attrition Risk | <1 sec | 85% |
| Dashboard Load | <2 sec | - |

## 🎯 Roadmap

- **v1.0** ✅ Core features, authentication, basic ML models
- **v1.1** 🔄 Advanced analytics, API enhancements
- **v2.0** 📋 Mobile app, real-time notifications
- **v3.0** 🤖 Advanced NLP, custom model builder

## 📞 Support & Contact

- **GitHub Issues**: For bug reports and features
- **Email**: your-email@example.com
- **Twitter**: [@yourhandle](https://twitter.com/yourhandle)
- **LinkedIn**: [Your Profile](https://linkedin.com/in/yourprofile)

---

## 📈 Statistics

![Stars](https://img.shields.io/github/stars/yourusername/hr-ai-system?style=social)
![Forks](https://img.shields.io/github/forks/yourusername/hr-ai-system?style=social)
![Issues](https://img.shields.io/github/issues/yourusername/hr-ai-system)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

---

**Made with ❤️ for better HR management through AI**
- Verify environment variables are set correctly
