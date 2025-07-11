from flask import render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length
from . import admin_bp  # Assuming admin_bp is defined in the package's __init__.py
from pkg.models import db, ResumeProfile, Experience, Education, Skill
from .auth import login_required

# --- Forms ---

class ProfileForm(FlaskForm):
    summary = TextAreaField('Summary', validators=[DataRequired()], render_kw={"class": "form-control textarea-large", "rows": 5})
    phone = StringField('Phone Number', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Email Address', validators=[DataRequired()], render_kw={"class": "form-control"})
    location = StringField('Location', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Update Profile', render_kw={"class": "btn-submit"})

class ExperienceForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()], render_kw={"class": "form-control"})
    company = StringField('Company', validators=[DataRequired()], render_kw={"class": "form-control"})
    date_range = StringField('Date Range (e.g., Jan 2025 – Present)', validators=[DataRequired()], render_kw={"class": "form-control"})
    tech_tags = StringField('Tech Tags (comma-separated)', render_kw={"class": "form-control"})
    description = TextAreaField('Description (one bullet point per line)', validators=[DataRequired()], render_kw={"class": "form-control textarea-large", "rows": 6})
    display_order = IntegerField('Display Order', default=0, render_kw={"class": "form-control"})
    submit = SubmitField('Save Experience', render_kw={"class": "btn-submit"})

class EducationForm(FlaskForm):
    institution = StringField('Institution/School', validators=[DataRequired()], render_kw={"class": "form-control"})
    degree = StringField('Degree/Certificate', validators=[DataRequired()], render_kw={"class": "form-control"})
    date_range = StringField('Date Range (e.g., 2025 - 2029)', validators=[DataRequired()], render_kw={"class": "form-control"})
    display_order = IntegerField('Display Order', default=0, render_kw={"class": "form-control"})
    submit = SubmitField('Save Education', render_kw={"class": "btn-submit"})

class SkillForm(FlaskForm):
    name = StringField('Skill Name (e.g., Python)', validators=[DataRequired()], render_kw={"class": "form-control"})
    category = SelectField('Category', choices=[
        ('Proficient', 'Proficient'),
        ('Frameworks & Libraries', 'Frameworks & Libraries'),
        ('Tools & Platforms', 'Tools & Platforms')
    ], validators=[DataRequired()], render_kw={"class": "form-control"})
    display_order = IntegerField('Display Order', default=0, render_kw={"class": "form-control"})
    submit = SubmitField('Save Skill', render_kw={"class": "btn-submit"})

# --- Routes ---

@admin_bp.route('/manage-resume', methods=['GET', 'POST'])
@login_required
def manage_resume():
    # There should only be one profile with id=1
    profile = ResumeProfile.query.get(1)
    if not profile:
        # Create a default profile if it doesn't exist
        profile = ResumeProfile(id=1, summary="Default summary.", phone="N/A", email="N/A", location="N/A")
        db.session.add(profile)
        db.session.commit()

    form = ProfileForm(obj=profile)
    if form.validate_on_submit():
        form.populate_obj(profile)
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin.manage_resume'))

    experiences = Experience.query.order_by(Experience.display_order).all()
    educations = Education.query.order_by(Education.display_order).all()
    skills = Skill.query.order_by(Skill.category, Skill.display_order).all()
    
    return render_template('admin/manage_resume.html', form=form, experiences=experiences, educations=educations, skills=skills)


# Generic Add/Edit/Delete logic for resume items
def get_model_and_form(item_type):
    if item_type == 'experience':
        return Experience, ExperienceForm, 'Experience'
    if item_type == 'education':
        return Education, EducationForm, 'Education'
    if item_type == 'skill':
        return Skill, SkillForm, 'Skill'
    return None, None, None

@admin_bp.route('/resume/<item_type>/add', methods=['GET', 'POST'])
@login_required
def add_resume_item(item_type):
    Model, Form, title = get_model_and_form(item_type)
    if not Model:
        return "Invalid item type", 404
        
    form = Form()
    if form.validate_on_submit():
        new_item = Model()
        form.populate_obj(new_item)
        db.session.add(new_item)
        db.session.commit()
        flash(f'{title} added successfully!', 'success')
        return redirect(url_for('admin.manage_resume'))
    return render_template('admin/add_edit_resume_item.html', form=form, title=f'Add New {title}')

@admin_bp.route('/resume/<item_type>/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_resume_item(item_type, item_id):
    Model, Form, title = get_model_and_form(item_type)
    if not Model:
        return "Invalid item type", 404
        
    item = Model.query.get_or_404(item_id)
    form = Form(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash(f'{title} updated successfully!', 'success')
        return redirect(url_for('admin.manage_resume'))
    return render_template('admin/add_edit_resume_item.html', form=form, title=f'Edit {title}')

@admin_bp.route('/resume/<item_type>/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_resume_item(item_type, item_id):
    Model, _, title = get_model_and_form(item_type)
    if not Model:
        return "Invalid item type", 404

    item = Model.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'{title} deleted successfully.', 'success')
    return redirect(url_for('admin.manage_resume'))