import os
from flask import render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL

from . import admin_bp
from pkg.models import db, Project
from .auth import login_required

# --- Form Definition ---
class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=100)])
    date = DateField('Completion Date', validators=[DataRequired()], format='%Y-%m-%d')
    description = TextAreaField('Description', validators=[DataRequired()])
    
    video = FileField('Project Video (MP4)', validators=[
        FileAllowed(['mp4'], 'Only MP4 videos are allowed!')
    ])
    poster = FileField('Poster Image (JPG, PNG)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPG and PNG images are allowed!')
    ])
    
    project_type = SelectField('Project Type', choices=[
        ('Personal', 'Personal'), 
        ('Client', 'Client'), 
        ('Collaborative', 'Collaborative')
    ], validators=[DataRequired()])
    
    tech_tags = StringField('Tech Used (comma-separated)', validators=[Optional(), Length(max=255)])
    role = StringField('Your Role', validators=[DataRequired(), Length(max=100)])
    
    ai_used = BooleanField('AI Was Used in this Project')
    ai_desc = StringField('How was AI used?', validators=[Optional(), Length(max=255)])
    
    # --- NEW & UPDATED FIELDS ---
    cost = StringField('Project Cost / Value', validators=[Optional(), Length(max=100)])
    client_name = StringField('Client Name (if applicable)', validators=[Optional(), Length(max=100)])
    live_url = StringField('Live Project URL', validators=[Optional(), URL()])
    github_url = StringField('GitHub Repository URL', validators=[Optional(), URL()])
    case_study_url = StringField('Case Study URL', validators=[Optional(), URL()])
    
    submit = SubmitField('Save Project')

# --- Helper Functions ---
def save_file(file, upload_folder):
    """Saves a file to the specified folder with a secure filename."""
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        return filename
    return None

def delete_file(filename, upload_folder):
    """Deletes a file if it exists."""
    if filename:
        try:
            os.remove(os.path.join(upload_folder, filename))
        except OSError as e:
            print(f"Error deleting file {filename}: {e}")

# --- Routes ---

@admin_bp.route('/projects')
@login_required
def manage_projects():
    """Displays all projects in a list."""
    projects = Project.query.order_by(Project.date.desc()).all()
    return render_template('admin/manage_projects.html', projects=projects)


@admin_bp.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    """Handles adding a new project."""
    form = ProjectForm()
    # On first load (GET), require files.
    if request.method == 'GET':
        form.video.validators = [FileRequired(), FileAllowed(['mp4'], 'Only MP4 videos are allowed!')]
        form.poster.validators = [FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')]

    if form.validate_on_submit():
        # Save uploaded files
        video_filename = save_file(form.video.data, current_app.config['UPLOAD_FOLDER_VIDEO'])
        poster_filename = save_file(form.poster.data, current_app.config['UPLOAD_FOLDER_IMAGE'])

        # Create new project instance
        new_project = Project(
            title=form.title.data,
            date=form.date.data,
            description=form.description.data,
            video_filename=video_filename,
            poster_filename=poster_filename,
            project_type=form.project_type.data,
            tech_tags=form.tech_tags.data,
            role=form.role.data,
            ai_used=form.ai_used.data,
            ai_desc=form.ai_desc.data,
            cost=form.cost.data,
            client_name=form.client_name.data,
            live_url=form.live_url.data,
            github_url=form.github_url.data,
            case_study_url=form.case_study_url.data
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Project has been successfully created!', 'success')
        return redirect(url_for('admin.manage_projects'))

    return render_template('admin/add_edit_project.html', form=form, legend='Add New Project')


@admin_bp.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Handles editing an existing project."""
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)
    
    # On edit, file uploads are optional
    form.video.validators = [Optional(), FileAllowed(['mp4'], 'Only MP4 videos are allowed!')]
    form.poster.validators = [Optional(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')]

    if form.validate_on_submit():
        # Handle file updates
        if form.video.data:
            delete_file(project.video_filename, current_app.config['UPLOAD_FOLDER_VIDEO'])
            project.video_filename = save_file(form.video.data, current_app.config['UPLOAD_FOLDER_VIDEO'])
        
        if form.poster.data:
            delete_file(project.poster_filename, current_app.config['UPLOAD_FOLDER_IMAGE'])
            project.poster_filename = save_file(form.poster.data, current_app.config['UPLOAD_FOLDER_IMAGE'])

        # Update fields from form
        project.title = form.title.data
        project.date = form.date.data
        project.description = form.description.data
        project.project_type = form.project_type.data
        project.tech_tags = form.tech_tags.data
        project.role = form.role.data
        project.ai_used = form.ai_used.data
        project.ai_desc = form.ai_desc.data
        project.cost = form.cost.data
        project.client_name = form.client_name.data
        project.live_url = form.live_url.data
        project.github_url = form.github_url.data
        project.case_study_url = form.case_study_url.data

        db.session.commit()
        flash('Project has been successfully updated!', 'success')
        return redirect(url_for('admin.manage_projects'))

    return render_template('admin/add_edit_project.html', form=form, legend=f'Edit "{project.title}"', project=project)


@admin_bp.route('/projects/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    """Handles deleting a project and its files."""
    project = Project.query.get_or_404(project_id)
    
    # Delete associated files first
    delete_file(project.video_filename, current_app.config['UPLOAD_FOLDER_VIDEO'])
    delete_file(project.poster_filename, current_app.config['UPLOAD_FOLDER_IMAGE'])
    
    # Delete project from DB
    db.session.delete(project)
    db.session.commit()
    
    flash('Project has been deleted.', 'success')
    return redirect(url_for('admin.manage_projects'))