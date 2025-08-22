from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    profile_image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    resumes = db.relationship('Resume', backref='user', lazy=True, cascade='all, delete-orphan')
    csv_uploads = db.relationship('CSVUpload', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def __repr__(self):
        return f'<User {self.username}>'

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    text_content = db.Column(db.Text)
    language = db.Column(db.String(10), default='en')
    
    # Relationship to analysis
    analyses = db.relationship('Analysis', backref='resume', lazy=True, cascade='all, delete-orphan')

class Analysis(db.Model):
    __tablename__ = 'analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    job_description = db.Column(db.Text)
    ats_score = db.Column(db.Float)
    extracted_skills = db.Column(db.Text)  # JSON string
    missing_keywords = db.Column(db.Text)  # JSON string
    suggestions = db.Column(db.Text)  # JSON string
    analysis_time = db.Column(db.DateTime, default=datetime.utcnow)

class CSVUpload(db.Model):
    __tablename__ = 'csv_uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    columns_info = db.Column(db.Text)  # JSON string
    stats_summary = db.Column(db.Text)  # JSON string
    row_count = db.Column(db.Integer)
    column_count = db.Column(db.Integer)
