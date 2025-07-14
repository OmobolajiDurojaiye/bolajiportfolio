from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, JSON, Text
from datetime import datetime, date as dt_date
from werkzeug.security import generate_password_hash, check_password_hash
from slugify import slugify

db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=dt_date.today)
    description = db.Column(db.Text, nullable=False)
    
    video_filename = db.Column(db.String(255), nullable=True)
    poster_filename = db.Column(db.String(255), nullable=True)
    
    project_type = db.Column(db.String(50), nullable=False)
    tech_tags = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(100), nullable=False)
    
    ai_used = db.Column(db.Boolean, default=False, nullable=False)
    ai_desc = db.Column(db.String(255), nullable=True)
    
    # --- NEW & UPDATED FIELDS ---
    cost = db.Column(db.String(100), nullable=True)
    client_name = db.Column(db.String(100), nullable=True)
    case_study_url = db.Column(db.String(255), nullable=True)
    live_url = db.Column(db.String(255), nullable=True)
    github_url = db.Column(db.String(255), nullable=True)
    
    @property
    def video_url(self):
        if self.video_filename:
            return url_for('static', filename=f'uploads/video/{self.video_filename}', _external=True)
        return None

    @property
    def poster_url(self):
        if self.poster_filename:
            return url_for('static', filename=f'uploads/image/{self.poster_filename}', _external=True)
        return url_for('static', filename='images/default_poster.jpg', _external=True)

    def __repr__(self):
        return f'<Project {self.title}>'

# --- NEW MODEL FOR BLOG POSTS ---
class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subtitle = db.Column(db.String(200), nullable=True)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    content = db.Column(Text, nullable=False)
    
    thumbnail_filename = db.Column(db.String(255), nullable=True)
    
    category = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.String(255), nullable=True)
    
    author = db.Column(db.String(100), nullable=False, default='Bolaji')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    read_time = db.Column(db.Integer, nullable=True) # in minutes
    status = db.Column(db.String(20), nullable=False, default='Draft') # Draft or Published
    
    meta_description = db.Column(db.String(160), nullable=True)

    @property
    def thumbnail_url(self):
        if self.thumbnail_filename:
            return url_for('static', filename=f'uploads/image/{self.thumbnail_filename}', _external=True)
        return url_for('static', filename='images/default_blog_thumb.jpg', _external=True) # Add a default thumbnail

    def __repr__(self):
        return f'<BlogPost {self.title}>'

# Auto-generate slug from title before committing
@event.listens_for(BlogPost, 'before_insert')
def receive_before_insert(mapper, connection, target):
    if target.title and not target.slug:
        # Create a unique slug
        base_slug = slugify(target.title)
        unique_slug = base_slug
        count = 1
        while BlogPost.query.filter_by(slug=unique_slug).first():
            unique_slug = f"{base_slug}-{count}"
            count += 1
        target.slug = unique_slug

class ContactSubmission(db.Model):
    __tablename__ = 'contact_submissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<ContactSubmission from {self.name}>'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class ResumeProfile(db.Model):
    __tablename__ = 'resume_profile'
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(Text, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(100), nullable=False)

class Experience(db.Model):
    __tablename__ = 'experience'
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    date_range = db.Column(db.String(100), nullable=False)
    description = db.Column(Text, nullable=False)
    tech_tags = db.Column(db.String(255), nullable=True)
    display_order = db.Column(db.Integer, default=0)

class Education(db.Model):
    __tablename__ = 'education'
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    date_range = db.Column(db.String(100), nullable=False)
    display_order = db.Column(db.Integer, default=0)

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    display_order = db.Column(db.Integer, default=0)