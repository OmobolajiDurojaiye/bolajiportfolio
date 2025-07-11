from . import main_bp
from flask import render_template, request, flash, redirect, url_for, jsonify, current_app, send_from_directory
from pkg.models import db, ResumeProfile, Experience, Education, Skill
from collections import defaultdict

@main_bp.route('/resume')
def resume():
    """Renders the interactive resume page."""
    profile = ResumeProfile.query.get(1)
    experiences = Experience.query.order_by(Experience.display_order.desc(), Experience.id.desc()).all()
    educations = Education.query.order_by(Education.display_order.desc(), Education.id.desc()).all()
    
    # Group skills by category
    skills_query = Skill.query.order_by(Skill.display_order, Skill.name).all()
    skills_by_category = defaultdict(list)
    for skill in skills_query:
        skills_by_category[skill.category].append(skill)

    return render_template('main/resume.html', 
                           profile=profile, 
                           experiences=experiences, 
                           educations=educations,
                           skills_by_category=skills_by_category)

# Add a route to handle the PDF download
@main_bp.route('/download-resume')
def download_resume():
    """Serves the resume PDF for download."""
    # IMPORTANT: Place your resume PDF in the 'static/documents' folder
    # Make sure to create the 'documents' folder inside 'static'
    try:
        return send_from_directory(
            'static/documents', 
            'Bolaji_Durojaiye_Resume.pdf', 
            as_attachment=True
        )
    except FileNotFoundError:
        flash('Resume file not found. Please contact me directly.', 'error')
        return redirect(url_for('main.resume'))