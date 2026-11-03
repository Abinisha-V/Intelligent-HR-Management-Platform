import os
from datetime import datetime
from urllib.parse import urlsplit
import click
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# ML Models
try:
    from models.resume_model.resume_model import get_resume_text, resume_match_score
    from models.performance_model.performance_model import predict_performance, load_performance_model
    from models.attrition_model.attrition_model import predict_attrition, load_attrition_model
    ML_MODELS_AVAILABLE = True
except ImportError as e:
    print(f"ML models not available: {e}")
    ML_MODELS_AVAILABLE = False
    # Dummy functions
    def get_resume_text(filepath):
        return "Sample resume text"
    def resume_match_score(text, job_desc):
        return 75.0
    def predict_performance(values):
        return "Average Performer"
    def load_performance_model():
        pass
    def predict_attrition(values):
        return {"risk": "Low", "probability": 0.2}
    def load_attrition_model():
        pass

# Flask setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)

# Database configuration
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    # MySQL example: mysql+pymysql://user:password@localhost/hr_ai
    DATABASE_URL = "sqlite:///hr_ai.db"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Upload configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"pdf", "docx"}

# Initialize DB & models
db = SQLAlchemy(app)

# Load ML models
# Moved to lazy loading to avoid serverless timeouts

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='hr')  # Only HR role for now

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class CandidateScreening(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    resume_filename = db.Column(db.String(250), nullable=False)
    score = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EmployeeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    tasks_completed = db.Column(db.Float, nullable=False)
    avg_completion_time = db.Column(db.Float, nullable=False)
    attendance = db.Column(db.Float, nullable=False)
    manager_rating = db.Column(db.Float, nullable=False)
    deadlines_missed = db.Column(db.Float, nullable=False)
    performance_prediction = db.Column(db.String(100), nullable=False)
    attrition_risk = db.Column(db.String(100), nullable=False)
    attrition_probability = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def initialize_database():
    if getattr(app, 'db_initialized', False):
        return

    db.create_all()
    if not User.query.filter_by(username='hr').first():
        hr_user = User(username='hr')
        hr_user.set_password('hr123')
        db.session.add(hr_user)
        db.session.commit()

    app.db_initialized = True


@app.before_request
def init_db():
    initialize_database()

    if not getattr(app, 'models_initialized', False):
        try:
            load_performance_model()
        except Exception as e:
            print(f"Performance model unavailable: {e}")

        try:
            load_attrition_model()
        except Exception as e:
            print(f"Attrition model unavailable: {e}")

        app.models_initialized = True


@app.cli.command("set-user-password")
@click.argument("username")
def set_user_password(username):
    """Set a user's password using hidden interactive prompts."""
    initialize_database()
    user = User.query.filter_by(username=username.strip()).first()
    if user is None:
        raise click.ClickException(f"User '{username}' does not exist.")

    password = click.prompt("New password", hide_input=True, confirmation_prompt=True)
    if not password:
        raise click.ClickException("Password cannot be empty.")

    user.set_password(password)
    db.session.commit()
    click.echo(f"Password updated for '{user.username}'.")


login_manager.init_app(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = request.form.get('password') or ''
        
        user = User.query.filter_by(username=username).first() if username else None
        if user and password and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                parsed_next = urlsplit(next_page)
                if (
                    next_page.startswith('/')
                    and not next_page.startswith('//')
                    and '\\' not in next_page
                    and not parsed_next.scheme
                    and not parsed_next.netloc
                ):
                    return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login'))


@app.route("/")
@login_required
def index():
    total_candidates = CandidateScreening.query.count()
    total_employees = EmployeeRecord.query.count()

    high_risk = EmployeeRecord.query.filter(EmployeeRecord.attrition_risk == "High").count()

    performance_counts = dict(
        db.session.query(EmployeeRecord.performance_prediction, db.func.count(EmployeeRecord.id))
        .group_by(EmployeeRecord.performance_prediction)
        .all()
    )

    attrition_counts = dict(
        db.session.query(EmployeeRecord.attrition_risk, db.func.count(EmployeeRecord.id))
        .group_by(EmployeeRecord.attrition_risk)
        .all()
    )

    return render_template(
        "index.html",
        total_candidates=total_candidates,
        total_employees=total_employees,
        high_risk=high_risk,
        performance_counts=performance_counts,
        attrition_counts=attrition_counts,
    )


@app.route("/resume", methods=["GET", "POST"])
@login_required
def resume_screen():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        job_description = request.form.get("job_description")
        file = request.files.get("resume")

        if not name or not email or not job_description or not file:
            flash("All fields are required for resume screening.", "danger")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Only PDF and DOCX resumes are supported.", "danger")
            return redirect(request.url)

        filename = secure_filename(f"{datetime.utcnow().timestamp()}_{file.filename}")
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        try:
            resume_text = get_resume_text(filepath)
            score = resume_match_score(resume_text, job_description)
            status = "Shortlisted" if score >= 75 else "Maybe" if score >= 50 else "Rejected"

            candidate = CandidateScreening(
                name=name,
                email=email,
                job_description=job_description,
                resume_filename=filename,
                score=score,
                status=status,
            )
            db.session.add(candidate)
            db.session.commit()

            flash(f"Resume screening completed: {status} ({score:.2f}%).", "success")
            return render_template("resume_result.html", candidate=candidate)

        except Exception as e:
            flash(f"Error processing resume: {str(e)}", "danger")
            return redirect(request.url)

    return render_template("resume_screen.html")


@app.route("/performance", methods=["GET", "POST"])
@login_required
def performance_predict():
    if request.method == "POST":
        name = request.form.get("name")
        role = request.form.get("role")
        values = [
            float(request.form.get("tasks_completed", 0)),
            float(request.form.get("avg_completion_time", 0)),
            float(request.form.get("attendance", 0)),
            float(request.form.get("manager_rating", 0)),
            float(request.form.get("deadlines_missed", 0)),
        ]

        if not name or not role:
            flash("Name and role are required.", "danger")
            return redirect(request.url)

        performance = predict_performance(values)
        attrition_outcome = predict_attrition(values)

        record = EmployeeRecord(
            name=name,
            role=role,
            tasks_completed=values[0],
            avg_completion_time=values[1],
            attendance=values[2],
            manager_rating=values[3],
            deadlines_missed=values[4],
            performance_prediction=performance,
            attrition_risk=attrition_outcome["risk"],
            attrition_probability=attrition_outcome["probability"],
        )
        db.session.add(record)
        db.session.commit()

        return render_template("performance_result.html", record=record)

    return render_template("performance.html")


@app.route("/analytics")
@login_required
def analytics():
    candidates = CandidateScreening.query.order_by(CandidateScreening.created_at.desc()).limit(5).all()
    employees = EmployeeRecord.query.order_by(EmployeeRecord.created_at.desc()).limit(5).all()

    performance_counts = dict(
        db.session.query(EmployeeRecord.performance_prediction, db.func.count(EmployeeRecord.id))
        .group_by(EmployeeRecord.performance_prediction)
        .all()
    )

    attrition_counts = dict(
        db.session.query(EmployeeRecord.attrition_risk, db.func.count(EmployeeRecord.id))
        .group_by(EmployeeRecord.attrition_risk)
        .all()
    )

    return render_template(
        "analytics.html",
        candidates=candidates,
        employees=employees,
        performance_counts=performance_counts,
        attrition_counts=attrition_counts,
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# REST API Endpoints
@app.route("/api/resume-screen", methods=["POST"])
def api_resume_screen():
    """API endpoint for resume screening"""
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ["name", "email", "job_description", "resume_text"]):
            return {"error": "Missing required fields: name, email, job_description, resume_text"}, 400

        from models.resume_model.resume_model import resume_match_score
        score = resume_match_score(data["resume_text"], data["job_description"])
        status = "Shortlisted" if score >= 75 else "Maybe" if score >= 50 else "Rejected"

        candidate = CandidateScreening(
            name=data["name"],
            email=data["email"],
            job_description=data["job_description"],
            resume_filename="api_upload",
            score=score,
            status=status,
        )
        db.session.add(candidate)
        db.session.commit()

        return {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "score": candidate.score,
            "status": candidate.status,
            "created_at": candidate.created_at.isoformat()
        }, 201

    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/api/performance-predict", methods=["POST"])
def api_performance_predict():
    """API endpoint for performance prediction"""
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ["name", "role", "tasks_completed", "avg_completion_time", "attendance", "manager_rating", "deadlines_missed"]):
            return {"error": "Missing required fields"}, 400

        values = [
            float(data["tasks_completed"]),
            float(data["avg_completion_time"]),
            float(data["attendance"]),
            float(data["manager_rating"]),
            float(data["deadlines_missed"])
        ]

        performance = predict_performance(values)
        attrition_outcome = predict_attrition(values)

        record = EmployeeRecord(
            name=data["name"],
            role=data["role"],
            tasks_completed=values[0],
            avg_completion_time=values[1],
            attendance=values[2],
            manager_rating=values[3],
            deadlines_missed=values[4],
            performance_prediction=performance,
            attrition_risk=attrition_outcome["risk"],
            attrition_probability=attrition_outcome["probability"],
        )
        db.session.add(record)
        db.session.commit()

        return {
            "id": record.id,
            "name": record.name,
            "role": record.role,
            "performance_prediction": record.performance_prediction,
            "attrition_risk": record.attrition_risk,
            "attrition_probability": record.attrition_probability,
            "created_at": record.created_at.isoformat()
        }, 201

    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/api/analytics", methods=["GET"])
def api_analytics():
    """API endpoint for analytics data"""
    try:
        total_candidates = CandidateScreening.query.count()
        total_employees = EmployeeRecord.query.count()
        high_risk = EmployeeRecord.query.filter(EmployeeRecord.attrition_risk == "High").count()

        performance_counts = dict(
            db.session.query(EmployeeRecord.performance_prediction, db.func.count(EmployeeRecord.id))
            .group_by(EmployeeRecord.performance_prediction)
            .all()
        )

        attrition_counts = dict(
            db.session.query(EmployeeRecord.attrition_risk, db.func.count(EmployeeRecord.id))
            .group_by(EmployeeRecord.attrition_risk)
            .all()
        )

        recent_candidates = [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "score": c.score,
                "status": c.status,
                "created_at": c.created_at.isoformat()
            } for c in CandidateScreening.query.order_by(CandidateScreening.created_at.desc()).limit(10).all()
        ]

        recent_employees = [
            {
                "id": r.id,
                "name": r.name,
                "role": r.role,
                "performance_prediction": r.performance_prediction,
                "attrition_risk": r.attrition_risk,
                "created_at": r.created_at.isoformat()
            } for r in EmployeeRecord.query.order_by(EmployeeRecord.created_at.desc()).limit(10).all()
        ]

        return {
            "summary": {
                "total_candidates": total_candidates,
                "total_employees": total_employees,
                "high_risk_employees": high_risk
            },
            "performance_distribution": performance_counts,
            "attrition_distribution": attrition_counts,
            "recent_candidates": recent_candidates,
            "recent_employees": recent_employees
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Export the app for Vercel deployment
application = app
